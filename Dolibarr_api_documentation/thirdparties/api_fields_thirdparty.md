# API Fields for Thirdparties

Complete list of fields available in Dolibarr API responses for thirdparties (customers, suppliers, prospects).

## Main Fields

| API Field | Type | Description |
|-----------|------|-------------|
| **id** / **rowid** | integer | Unique ID of the thirdparty |
| **name** / **nom** | string | Company name (required) |
| **name_alias** | string | Alternative name/alias |
| **ref_ext** | string | External reference |
| **entity** | integer | Multi-company entity ID |

## Contact Information

| API Field | Type | Description |
|-----------|------|-------------|
| **address** | string | Street address |
| **zip** | string | Postal/ZIP code |
| **town** | string | City/Town |
| **state_id** / **fk_departement** | integer | State/Department ID |
| **state** / **departement** | string | State/Department name |
| **state_code** / **departement_code** | string | State/Department code |
| **country_id** / **fk_pays** | integer | Country ID |
| **country** / **pays** | string | Country name |
| **country_code** | string | Country ISO code (e.g., 'US', 'FR') |
| **phone** | string | Main phone number |
| **phone_pro** | string | Professional phone number |
| **fax** | string | Fax number |
| **email** | string | Email address |
| **url** | string | Website URL |
| **socialnetworks** | object/text | Social network links |
| **skype** | string | Skype username |
| **twitter** | string | Twitter handle |
| **facebook** | string | Facebook profile |
| **linkedin** | string | LinkedIn profile |
| **instagram** | string | Instagram handle |
| **youtube** | string | YouTube channel |
| **whatsapp** | string | WhatsApp number |

## Customer/Supplier Information

| API Field | Type | Description |
|-----------|------|-------------|
| **client** | integer | Customer type: 0=none, 1=customer, 2=prospect, 3=customer+prospect |
| **fournisseur** | integer | Supplier: 0=no, 1=yes |
| **code_client** | string | Customer code (unique) |
| **code_fournisseur** | string | Supplier code (unique) |
| **code_compta** | string | Customer accounting code |
| **code_compta_fournisseur** | string | Supplier accounting code |
| **fk_prospectlevel** | string | Prospect level ID |
| **fk_stcomm** | integer | Commercial status ID |
| **stcomm_id** | integer | Commercial status ID (alias) |
| **status_prospect_label** | string | Prospect status label |

## Professional Identification

| API Field | Type | Description |
|-----------|------|-------------|
| **idprof1** / **siren** | string | Professional ID 1 (SIREN in France) |
| **idprof2** / **siret** | string | Professional ID 2 (SIRET in France) |
| **idprof3** / **ape** | string | Professional ID 3 (APE/NAF in France) |
| **idprof4** | string | Professional ID 4 (RCS in France) |
| **idprof5** | string | Professional ID 5 |
| **idprof6** | string | Professional ID 6 |
| **tva_intra** | string | Intra-community VAT number |
| **tva_assuj** | integer | Subject to VAT: 0=no, 1=yes |

## Company Details

| API Field | Type | Description |
|-----------|------|-------------|
| **capital** | float | Company capital |
| **fk_effectif** | integer | Workforce/number of employees ID |
| **effectif_id** | integer | Workforce ID (alias) |
| **fk_typent** | integer | Company type ID |
| **typent_id** | integer | Company type ID (alias) |
| **typent_code** | string | Company type code |
| **fk_forme_juridique** | integer | Legal form ID |
| **forme_juridique_code** | string | Legal form code |
| **forme_juridique** | string | Legal form label |

## Financial Settings

| API Field | Type | Description |
|-----------|------|-------------|
| **remise_percent** | float | Default discount percentage |
| **remise_supplier_percent** | float | Default supplier discount percentage |
| **mode_reglement_id** | integer | Payment method ID |
| **cond_reglement_id** | integer | Payment terms ID |
| **deposit_percent** | float | Default deposit percentage |
| **mode_reglement_supplier_id** | integer | Supplier payment method ID |
| **cond_reglement_supplier_id** | integer | Supplier payment terms ID |
| **transport_mode_supplier_id** | integer | Supplier transport mode ID |
| **fk_multicurrency** | integer | Multi-currency ID |
| **multicurrency_code** | string | Currency code |
| **price_level** | integer | Price level (for multiprices) |
| **outstanding_limit** | float | Outstanding amount limit |

## Accounting & Banking

| API Field | Type | Description |
|-----------|------|-------------|
| **fk_account** | integer | Default bank account ID |
| **bank_account** | string | Bank account number |
| **localtax1_assuj** | integer | Subject to local tax 1 |
| **localtax1_value** | float | Local tax 1 rate |
| **localtax2_assuj** | integer | Subject to local tax 2 |
| **localtax2_value** | float | Local tax 2 rate |

## Incoterms

| API Field | Type | Description |
|-----------|------|-------------|
| **fk_incoterms** | integer | Incoterm type ID |
| **location_incoterms** | string | Incoterm location |
| **label_incoterms** | string | Incoterm label |

## Barcode

| API Field | Type | Description |
|-----------|------|-------------|
| **barcode** | string | Barcode value |
| **barcode_type** | integer | Barcode type ID |
| **barcode_type_code** | string | Barcode type code |
| **barcode_type_label** | string | Barcode type label |
| **barcode_type_coder** | string | Barcode type coder |

## Dates

| API Field | Type | Description |
|-----------|------|-------------|
| **datec** / **date_creation** / **date_c** | integer | Creation date (Unix timestamp) |
| **tms** / **date_modification** / **date_m** | integer | Last modification date (Unix timestamp) |

## User Tracking

| API Field | Type | Description |
|-----------|------|-------------|
| **user_creation_id** / **fk_user_creat** | integer | ID of user who created the record |
| **user_modification_id** / **fk_user_modif** | integer | ID of user who last modified the record |

## Notes

| API Field | Type | Description |
|-----------|------|-------------|
| **note_public** | string | Public notes (visible to customer) |
| **note_private** | string | Private notes (internal only) |

## Parent Company

| API Field | Type | Description |
|-----------|------|-------------|
| **parent** | integer | Parent company ID |
| **parent_name** | string | Parent company name |

## Project Reference

| API Field | Type | Description |
|-----------|------|-------------|
| **fk_projet** | integer | Default project ID |

## Sales Representatives

| API Field | Type | Description |
|-----------|------|-------------|
| **commercial_id** | integer | Sales representative ID (used in create/update only) |

## Calculated/Computed Fields

| API Field | Type | Description |
|-----------|------|-------------|
| **absolute_discount** | float | Total available absolute discount (excluding credit notes) |
| **absolute_creditnote** | float | Total available credit note amount |
| **logo** | string | Path to company logo file |
| **logo_small** | string | Path to small logo file |
| **logo_mini** | string | Path to mini logo file |

## Status Indicators

| API Field | Type | Description |
|-----------|------|-------------|
| **status** | integer | General status |
| **import_key** | string | Import key for bulk operations |
| **array_options** | object | Custom fields (extra fields) |

## Document Management

| API Field | Type | Description |
|-----------|------|-------------|
| **model_pdf** | string | PDF template model name |
| **last_main_doc** | string | Path to last main document |

## Prefix (if enabled)

| API Field | Type | Description |
|-----------|------|-------------|
| **prefix_comm** | string | Commercial prefix (if SOCIETE_USEPREFIX is enabled) |

## Technical Fields

| API Field | Type | Description |
|-----------|------|-------------|
| **specimen** | integer | Is specimen record: 0=no, 1=yes |
| **validateFieldsErrors** | array | Validation errors |
| **table_element** | string | Database table name |
| **element** | string | Element type identifier |
| **fk_element** | string | Foreign key field name |
| **ismultientitymanaged** | integer | Multi-entity management flag |
| **linkedObjectsIds** | object | IDs of linked objects |
| **linked_objects** | object | Linked objects data |
| **oldcopy** | object | Copy of object before modification |

## Fields NOT returned by API (cleaned)

The following fields are removed from API responses for security/clarity:

- `nom` (deprecated, use `name`)
- `name_bis` (deprecated, use `name_alias`)
- `note` (deprecated, use `note_public` or `note_private`)
- `departement` (use `state`)
- `departement_code` (use `state_code`)
- `pays` (use `country`)
- `particulier`
- `prefix_comm` (unless enabled)
- `commercial_id` (only for create/update, not read)
- `total_ht`, `total_tva`, `total_ttc` (order/invoice totals)
- `lines` (invoice/order lines)
- `thirdparty` (recursive reference)
- `fk_delivery_address` (deprecated)
- Social network fields (cleaned individually)

## Important Notes

### For API Requests

When creating or updating thirdparties via API:

**Required fields:**
- `name` - Always required

**Conditionally required:**
- `email` - Required if `SOCIETE_EMAIL_MANDATORY` is enabled

### Field Usage Examples

**Essential fields:**
```
id,name,email,client,fournisseur,code_client
```

**With contact information:**
```
id,name,email,phone,address,zip,town,country_code
```

**With professional IDs:**
```
id,name,idprof1,idprof2,idprof3,tva_intra
```

**With financial info:**
```
id,name,code_client,code_compta,remise_percent,price_level
```

**Complete record:**
```
id,name,name_alias,email,phone,address,zip,town,country_id,client,fournisseur,code_client,code_fournisseur,idprof1,idprof2,tva_intra,note_public,note_private
```

## Client Type Values

| Value | Description |
|-------|-------------|
| 0 | Not a customer/prospect |
| 1 | Customer |
| 2 | Prospect |
| 3 | Customer and prospect |

## Supplier Type Values

| Value | Description |
|-------|-------------|
| 0 | Not a supplier |
| 1 | Supplier |

## Country-Specific Professional IDs

### France
- `idprof1` = SIREN (9 digits)
- `idprof2` = SIRET (14 digits)
- `idprof3` = APE/NAF code
- `idprof4` = RCS (Trade register)

### Spain
- `idprof1` = CIF/NIF
- `idprof2` = Registro Mercantil
- `idprof3` = CNAE

### United States
- `idprof1` = EIN (Employer Identification Number)
- `idprof2` = State registration number
- `idprof3` = NAICS code

### United Kingdom
- `idprof1` = Company Registration Number
- `idprof2` = VAT Registration Number

### Other Countries
Check Dolibarr's country-specific setup for professional ID field meanings.

## Extra Fields (array_options)

Custom fields are returned in the `array_options` object with keys like:
- `options_fieldname`

Example:
```json
{
  "array_options": {
    "options_custom_rating": "A+",
    "options_custom_segment": "Premium"
  }
}
```

## Social Networks Object

The `socialnetworks` field can contain:
```json
{
  "socialnetworks": {
    "skype": "companyskype",
    "twitter": "@company",
    "facebook": "company-page",
    "linkedin": "company/linkedin",
    "instagram": "@company_insta",
    "youtube": "CompanyChannel",
    "whatsapp": "+1234567890"
  }
}
```

## Usage in API Calls

### GET Requests
All fields are returned automatically (except cleaned fields).

### POST/PUT Requests
Send only the fields you want to set/update:

```json
{
  "name": "ACME Corporation",
  "email": "contact@acme.com",
  "client": 1,
  "address": "123 Business St",
  "zip": "12345",
  "town": "New York",
  "country_id": 1,
  "phone": "+1234567890",
  "idprof1": "123456789",
  "tva_intra": "FR12345678901"
}
```

### Filtering in List Requests
Use field names in SQL filters:

```
sqlfilters=(t.nom:like:'ACME%')and(t.client:=:1)
```

Note: Use table alias `t.` for thirdparty table fields in SQL filters.
