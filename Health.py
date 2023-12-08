import json
import google.auth
from google.cloud import language_v1
from google.cloud.language_v1 import types
from google.oauth2 import service_account

key_path = "/home/todd/googlework/credent/health-care-407504-f50fbe3d202b.json"

credentials = service_account.Credentials.from_service_account_file(key_path)
client = language_v1.LanguageServiceClient(credentials=credentials)

# Text
text_content = ("Patient John Doe, a 45-year-old male, presented to the clinic with symptoms of chronic cough and shortness of breath."
                " He has a history of asthma and was previously treated with Albuterol. However, due to recent exacerbations, his "
                "treatment plan has been revised to include a daily dose of Fluticasone and Salmeterol, along with the use of a "
                "rescue inhaler as needed for acute symptoms. John also reported occasional mild chest pain, for which an ECG was "
                "performed, revealing no significant abnormalities. His current list of medications includes Fluticasone, Salmeterol, "
                "and Aspirin. Follow-up in 4 weeks is recommended to monitor his response to the new treatment regimen.")


# Request to the Healthcare Natural Language API
document = types.Document(
    content=text_content,
    type_=language_v1.Document.Type.PLAIN_TEXT
)
encoding_type = language_v1.EncodingType.UTF8

# Calling the API
response = client.analyze_entities(document=document, encoding_type=encoding_type)

# Entity types
entity_type_names = {
    1: 'UNKNOWN',
    2: 'PERSON',
    3: 'LOCATION',
    4: 'ORGANIZATION',
    5: 'EVENT',
    6: 'WORK_OF_ART',
    7: 'CONSUMER_GOOD',
    8: 'OTHER',
    9: 'PHONE_NUMBER',
    10: 'ADDRESS',
    11: 'DATE',
    12: 'NUMBER',
    13: 'PRICE',
}
mention_type_names = {
    1: 'Unknown',
    2: 'Proper name',
    3: 'Common noun'
}

# output
for entity in response.entities:
    entity_type_name = entity_type_names.get(entity.type_, 'UNKNOWN')  # Get the entity type name from the mapping
    print(f"Entity: {entity.name}, Type: {entity_type_name}, Salience: {entity.salience}")
    for metadata_name, metadata_value in entity.metadata.items():
        print(f"{metadata_name}: {metadata_value}")

    for mention in entity.mentions:
        mention_type_name = mention_type_names.get(mention.type, 'UNKNOWN')
        print(f"Mention: {mention.text.content}, Type: {mention_type_name}")

