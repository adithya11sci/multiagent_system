"""
Validator Agent
Validates data authenticity and prevents hallucination
"""
from typing import Dict, Any, List, Optional
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
import json
import re
from datetime import datetime

from config import settings


class ValidationResult:
    """Validation result structure"""
    def __init__(
        self,
        is_valid: bool,
        confidence: float,
        issues: List[str],
        warnings: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.is_valid = is_valid
        self.confidence = confidence
        self.issues = issues
        self.warnings = warnings
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "confidence": self.confidence,
            "issues": self.issues,
            "warnings": self.warnings,
            "metadata": self.metadata
        }


class ValidatorAgent:
    """
    Validator Agent - Anti-Hallucination Layer
    
    Responsibilities:
    1. Verify data authenticity
    2. Check if email is genuine
    3. Validate extracted data
    4. Cross-check facts
    5. Flag suspicious data
    """
    
    def __init__(self):
        self.llm = ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0
        )
        
        self.system_prompt = """You are a data validation agent focused on preventing hallucination and ensuring data accuracy.

Your role is to:
1. Verify if extracted data is authentic and accurate
2. Check for inconsistencies or red flags
3. Validate against source material
4. Flag any suspicious or uncertain data
5. Provide confidence scores

Validation Criteria:
- Data matches source material exactly
- No made-up or guessed values
- Dates are realistic and properly formatted
- Amounts are numeric and reasonable
- Email/document appears authentic

Output Format (JSON):
{
    "is_valid": true/false,
    "confidence": 0.95,
    "issues": ["list of validation issues"],
    "warnings": ["list of warnings"],
    "validation_details": {
        "field_name": {
            "valid": true/false,
            "reason": "explanation"
        }
    }
}
"""
    
    async def validate(
        self,
        extracted_data: Dict[str, Any],
        source_text: str,
        validation_type: str = "general",
        strict: bool = True
    ) -> ValidationResult:
        """
        Validate extracted data against source
        
        Args:
            extracted_data: Data that was extracted
            source_text: Original source text
            validation_type: Type of validation to perform
            strict: If True, apply stricter validation rules
        """
        if validation_type == "bill":
            return await self._validate_bill_data(extracted_data, source_text, strict)
        elif validation_type == "email":
            return await self._validate_email_data(extracted_data, source_text, strict)
        else:
            return await self._validate_general(extracted_data, source_text, strict)
    
    async def _validate_general(
        self,
        extracted_data: Dict[str, Any],
        source_text: str,
        strict: bool
    ) -> ValidationResult:
        """General validation using LLM"""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""Source Text:
---
{source_text}
---

Extracted Data:
{json.dumps(extracted_data, indent=2)}

Strict Mode: {strict}

Validate if the extracted data accurately reflects the source text.
Check for hallucinations, inconsistencies, or errors.""")
        ]
        
        response = await self.llm.apredict_messages(messages)
        
        try:
            result = json.loads(response.content)
            return ValidationResult(
                is_valid=result.get("is_valid", False),
                confidence=result.get("confidence", 0.0),
                issues=result.get("issues", []),
                warnings=result.get("warnings", []),
                metadata=result.get("validation_details", {})
            )
        except json.JSONDecodeError:
            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                issues=["Failed to parse validation result"],
                warnings=[],
                metadata={"raw_response": response.content}
            )
    
    async def _validate_bill_data(
        self,
        extracted_data: Dict[str, Any],
        source_text: str,
        strict: bool
    ) -> ValidationResult:
        """Specialized validation for bill data"""
        issues = []
        warnings = []
        confidence = 1.0
        
        # Check if amount is numeric
        if "amount" in extracted_data:
            amount_data = extracted_data["amount"]
            amount_value = amount_data.get("value", "") if isinstance(amount_data, dict) else amount_data
            
            # Extract numeric value
            numeric_match = re.search(r'[\d,]+\.?\d*', str(amount_value))
            if not numeric_match:
                issues.append("Amount is not numeric")
                confidence *= 0.5
            else:
                # Check if amount appears in source
                if str(amount_value) not in source_text:
                    issues.append("Amount not found in source text")
                    confidence *= 0.7
        
        # Validate date
        if "date" in extracted_data:
            date_data = extracted_data["date"]
            date_value = date_data.get("value", "") if isinstance(date_data, dict) else date_data
            
            # Check if date is realistic
            try:
                # Try to parse date
                current_year = datetime.now().year
                if str(current_year) not in str(date_value):
                    # Check if it's a recent year
                    year_match = re.search(r'20\d{2}', str(date_value))
                    if year_match:
                        year = int(year_match.group())
                        if abs(year - current_year) > 2:
                            warnings.append(f"Date is from {year}, which may be old")
            except:
                pass
        
        # Check provider/company name
        if "provider" in extracted_data or "company" in extracted_data:
            provider_field = "provider" if "provider" in extracted_data else "company"
            provider_data = extracted_data[provider_field]
            provider_value = provider_data.get("value", "") if isinstance(provider_data, dict) else provider_data
            
            if provider_value and provider_value.lower() not in source_text.lower():
                warnings.append(f"{provider_field.title()} name may not match source")
                confidence *= 0.9
        
        # Use LLM for deeper validation if strict mode
        if strict:
            llm_result = await self._validate_general(extracted_data, source_text, strict)
            issues.extend(llm_result.issues)
            warnings.extend(llm_result.warnings)
            confidence = min(confidence, llm_result.confidence)
        
        is_valid = len(issues) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            confidence=confidence,
            issues=issues,
            warnings=warnings,
            metadata={"validation_type": "bill"}
        )
    
    async def _validate_email_data(
        self,
        extracted_data: Dict[str, Any],
        source_text: str,
        strict: bool
    ) -> ValidationResult:
        """Validate email authenticity"""
        issues = []
        warnings = []
        confidence = 1.0
        
        # Check for common phishing indicators
        phishing_patterns = [
            r'urgent.*action.*required',
            r'verify.*account',
            r'click.*here.*immediately',
            r'suspended.*account',
            r'unusual.*activity'
        ]
        
        source_lower = source_text.lower()
        for pattern in phishing_patterns:
            if re.search(pattern, source_lower):
                warnings.append(f"Potential phishing indicator: {pattern}")
                confidence *= 0.8
        
        # Validate email addresses
        if "from" in extracted_data or "sender" in extracted_data:
            email_field = "from" if "from" in extracted_data else "sender"
            email_value = extracted_data[email_field]
            
            # Basic email validation
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            if not re.search(email_pattern, str(email_value)):
                issues.append("Invalid email address format")
                confidence *= 0.5
        
        is_valid = len(issues) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            confidence=confidence,
            issues=issues,
            warnings=warnings,
            metadata={"validation_type": "email"}
        )
    
    def quick_validate(
        self,
        data: Any,
        expected_type: str
    ) -> bool:
        """Quick validation for data types"""
        if expected_type == "numeric":
            return bool(re.search(r'\d', str(data)))
        elif expected_type == "date":
            return bool(re.search(r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}', str(data)))
        elif expected_type == "email":
            return bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', str(data)))
        elif expected_type == "not_empty":
            return bool(data and str(data).strip())
        return True


# Global validator agent instance
validator_agent = ValidatorAgent()
