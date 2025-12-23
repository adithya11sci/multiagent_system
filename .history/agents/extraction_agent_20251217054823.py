"""
Extraction Agent
Extracts structured data from unstructured text/documents
"""
from typing import Dict, Any, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import json
import re

from config import settings


class ExtractionAgent:
    """
    Extraction Agent
    
    Responsibilities:
    1. Extract structured data from emails, PDFs, text
    2. Use LLM + regex + rules
    3. Handle OCR if needed
    4. Return structured JSON data
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0
        )
        
        self.system_prompt = """You are an expert data extraction agent.

Your role is to extract specific information from unstructured text with high accuracy.

Rules:
1. Extract ONLY the requested fields
2. Return structured JSON format
3. If a field is not found, use null
4. Include confidence score (0.0 to 1.0) for each field
5. Provide source text where data was found
6. Do NOT hallucinate or guess values
7. If uncertain, mark confidence as low

Output Format:
{
    "extracted_data": {
        "field_name": {
            "value": "extracted value",
            "confidence": 0.95,
            "source": "text snippet where found"
        }
    },
    "extraction_summary": "Brief summary of what was extracted"
}
"""
    
    async def extract(
        self,
        text: str,
        fields: List[str],
        extraction_type: str = "general",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract specific fields from text
        
        Args:
            text: Source text to extract from
            fields: List of field names to extract
            extraction_type: Type of extraction (email, bill, invoice, etc.)
            context: Additional context for extraction
        """
        # Choose extraction strategy
        if extraction_type == "bill" or extraction_type == "invoice":
            return await self._extract_bill_info(text, fields)
        elif extraction_type == "email":
            return await self._extract_email_info(text, fields)
        else:
            return await self._extract_general(text, fields, context)
    
    async def _extract_general(
        self,
        text: str,
        fields: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """General extraction using LLM"""
        fields_str = ", ".join(fields)
        context_str = json.dumps(context) if context else "None"
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""Text to extract from:
---
{text}
---

Fields to extract: {fields_str}
Additional context: {context_str}

Extract the requested fields and return structured JSON.""")
        ]
        
        response = await self.llm.apredict_messages(messages)
        
        try:
            result = json.loads(response.content)
            return result
        except json.JSONDecodeError:
            return {
                "extracted_data": {},
                "error": "Failed to parse extraction result",
                "raw_response": response.content
            }
    
    async def _extract_bill_info(
        self,
        text: str,
        fields: List[str]
    ) -> Dict[str, Any]:
        """Specialized extraction for bills/invoices"""
        # First, try regex patterns for common bill fields
        extracted_data = {}
        
        # Amount patterns
        if "amount" in fields or "bill_amount" in fields or "total" in fields:
            amount_patterns = [
                r'[₹$€£]\s*[\d,]+\.?\d*',
                r'(?:total|amount|bill)[\s:]*[₹$€£]?\s*[\d,]+\.?\d*',
                r'(?:total|amount)[\s:]*(?:rs\.?|inr)?\s*[\d,]+\.?\d*'
            ]
            
            for pattern in amount_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    extracted_data["amount"] = {
                        "value": matches[-1],  # Usually last occurrence is total
                        "confidence": 0.9,
                        "source": f"Regex pattern: {pattern}",
                        "method": "regex"
                    }
                    break
        
        # Date patterns
        if "date" in fields or "billing_date" in fields or "due_date" in fields:
            date_patterns = [
                r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
                r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',
                r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    extracted_data["date"] = {
                        "value": matches[0],
                        "confidence": 0.85,
                        "source": f"Regex pattern: {pattern}",
                        "method": "regex"
                    }
                    break
        
        # Use LLM for remaining fields
        remaining_fields = [f for f in fields if f not in extracted_data]
        
        if remaining_fields:
            llm_result = await self._extract_general(text, remaining_fields)
            if "extracted_data" in llm_result:
                extracted_data.update(llm_result["extracted_data"])
        
        return {
            "extracted_data": extracted_data,
            "extraction_summary": f"Extracted {len(extracted_data)} fields from bill/invoice"
        }
    
    async def _extract_email_info(
        self,
        text: str,
        fields: List[str]
    ) -> Dict[str, Any]:
        """Specialized extraction for email content"""
        # Email-specific extraction logic
        return await self._extract_general(text, fields, {"type": "email"})
    
    def extract_with_regex(
        self,
        text: str,
        patterns: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Extract using custom regex patterns
        
        Args:
            text: Source text
            patterns: Dict of {field_name: regex_pattern}
        """
        extracted_data = {}
        
        for field_name, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                extracted_data[field_name] = {
                    "value": matches[0] if len(matches) == 1 else matches,
                    "confidence": 0.95,
                    "source": f"Regex: {pattern}",
                    "method": "regex"
                }
            else:
                extracted_data[field_name] = {
                    "value": None,
                    "confidence": 0.0,
                    "source": "Not found",
                    "method": "regex"
                }
        
        return {
            "extracted_data": extracted_data,
            "extraction_summary": f"Regex extraction completed for {len(patterns)} patterns"
        }


# Global extraction agent instance
extraction_agent = ExtractionAgent()
