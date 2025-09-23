import logging
from models import BusinessCardData
from datetime import datetime

logger = logging.getLogger(__name__)

class VCardService:
    """Service class for generating vCard files from business card data manually"""

    def generate_vcard(self, data: BusinessCardData) -> str:
        try:
            lines = [
                "BEGIN:VCARD",
                "VERSION:3.0",
                f"N:{data.last_name or ''};{data.first_name or ''};{data.middle_name or ''};;",
                f"FN:{(data.first_name + ' ' + (data.middle_name or '') + ' ' + data.last_name).strip()}",
                f"ORG:{data.company_name or ''}",
                f"TITLE:{data.position or ''}",
                f"X-DEPARTMENT:{data.department or ''}",
            ]
            
            if data.mobile:
                for number in data.mobile:
                    lines.append(f"TEL;TYPE=CELL:{number}")
            if data.telephone:
                for number in data.telephone:
                    phone_val = number
                    if data.extension:
                        phone_val += f" ext. {data.extension}"
                    lines.append(f"TEL;TYPE=WORK:{phone_val}")
            if data.email:
                for email_addr in data.email:
                    lines.append(f"EMAIL;TYPE=WORK:{email_addr}")
            if data.website:
                for site in data.website:
                    website_str = str(site)
                    if not website_str.startswith(('http://', 'https://')):
                        website_str = f"https://{website_str}"
                    lines.append(f"URL:{website_str}")

            if data.address:
                adr_escaped = data.address.replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")
                lines.append(f"ADR;TYPE=WORK:;;{adr_escaped};;;;")
            if data.notes:
                notes_escaped = data.notes.replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")
                lines.append(f"NOTE:{notes_escaped}")

            rev_str = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            lines.append(f"REV:{rev_str}")
            lines.append("END:VCARD")

            vcard_text = "\r\n".join(lines)
            return vcard_text

        except Exception as e:
            logger.error(f"Failed to generate manual vCard: {str(e)}")
            raise

    def combine_vcards(self, vcards: list[str]) -> str:
        return "\r\n".join(vcards)

vcard_service = VCardService()