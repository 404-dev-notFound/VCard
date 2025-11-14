import os
import json
import logging
import google.generativeai as genai
from config import config
from models import BusinessCardData

logger = logging.getLogger(__name__)

class BusinessCardParser:
    def __init__(self):
        # Configure the SDK with the API key from your config
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            # Initialize the model. You can also use 'gemini-2.5-flash' for faster response.
            self.model = genai.GenerativeModel('gemini-2.5-pro')
            logger.info("Gemini Pro model initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to configure Gemini SDK: {e}")
            self.model = None

    def extract_business_card_data(self, text: str):
        """Extract structured data from OCR text using the Gemini Pro SDK"""
        if not self.model:
            logger.error("Gemini model is not initialized. Cannot process text.")
            return None

        try:
            # The prompt is the same as before
            prompt = f"""
You are an expert information extractor specializing in business cards. Your task is to extract fields from the given text and return ONLY a valid JSON object.

### DATA FIELDS
- **first_name** (string, required): The person's first name.
- **middle_name** (string, optional): The person's middle name or initial.
- **last_name** (string, required): The person's last name.
- **company_name** (string, required): The company or organization name.
- **position** (string, required): The job title or position.
- **department** (string, optional): The department or division.
- **mobile** (array of strings, optional): A list of all mobile/cell phone numbers.
- **telephone** (array of strings, optional): A list of all office/work phone numbers.
- **email** (array of strings, optional): A list of all email addresses.
- **website** (array of strings, optional): A list of all company website URLs.
- **address** (string, optional): The full business address.
- **extension** (string, optional): The phone extension number.
- **notes** (string, optional): Any additional information that doesn't fit other fields (e.g., fax numbers, certifications, slogans).

### IMPORTANT INSTRUCTIONS
1.  **JSON Only**: Your entire output must be a single, valid JSON object, with no explanatory text or markdown formatting around it.
2.  **Handle Multiple Values**: If you find more than one value for `mobile`, `telephone`, `email`, or `website`, you **must** return them as a JSON array of strings. If you find only one, return it as an array with a single string.
3.  **Handle Missing Values**: For optional fields that are not found, use `null`. For required fields that are not found, use an empty string `""`.
4.  **Identify Websites**: Correctly identify any website, such as `www.example.com` or `example.com`, and place it in the `website` field.
5.  **Consolidate Notes**: Combine all other miscellaneous text into the single `notes` field.

---

### BUSINESS CARD TEXT TO PROCESS:
{text}

### JSON OUTPUT:
"""
            response = self.model.generate_content(prompt)
            model_text = response.text.strip().replace("```json", "").replace("```", "").strip()

            if not model_text.startswith('{'):
                logger.error(f"LLM did not return a valid JSON object. Output: {model_text}")
                return None
            
            parsed_data = json.loads(model_text)
            logger.debug(f"Parsed JSON from LLM: {parsed_data}")

            # 1. Ensure fields that should be lists are lists
            list_fields = ['mobile', 'telephone', 'email', 'website']
            for field in list_fields:
                if field in parsed_data and parsed_data[field] and isinstance(parsed_data[field], str):
                    # If the LLM returned a string, wrap it in a list
                    parsed_data[field] = [parsed_data[field]]

            # 2. Prepend 'https://' to websites if the scheme is missing
            if 'website' in parsed_data and parsed_data['website']:
                sanitized_websites = []
                for site in parsed_data['website']:
                    if site and not site.startswith(('http://', 'https://')):
                        sanitized_websites.append(f"https://{site}")
                    else:
                        sanitized_websites.append(site)
                parsed_data['website'] = sanitized_websites

            # ✅ NEW DEBUG LINE: Let's see the data right before validation
            logger.info(f"FINAL DATA BEFORE VALIDATION: {parsed_data}")
            
            business_card = BusinessCardData(**parsed_data)
            logger.info("Successfully parsed business card data with Gemini")
            return business_card

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return None

# Singleton instance
parser_service = BusinessCardParser()
