# Thirdparties API

The Thirdparties API allows you to manage third parties (customers, suppliers, prospects) in your Dolibarr instance. You can create, read, update, delete thirdparties, and manage their related information such as categories, bank accounts, and gateway accounts.

## Endpoints

- [Get a thirdparty](#get-a-thirdparty)
- [Get thirdparty by email](#get-thirdparty-by-email)
- [Get thirdparty by barcode](#get-thirdparty-by-barcode)
- [List thirdparties](#list-thirdparties)
- [Create a thirdparty](#create-a-thirdparty)
- [Update a thirdparty](#update-a-thirdparty)
- [Merge thirdparties](#merge-thirdparties)
- [Delete a thirdparty](#delete-a-thirdparty)
- [Set price level](#set-price-level)
- [Customer Categories](#customer-categories)
- [Supplier Categories](#supplier-categories)
- [Outstanding Documents](#outstanding-documents)
- [Sales Representatives](#sales-representatives)
- [Fixed Amount Discounts](#fixed-amount-discounts)
- [Invoices for Replacement/Credit Note](#invoices-for-replacementcredit-note)
- [Bank Accounts](#bank-accounts)
- [Gateway Accounts](#gateway-accounts)

---

## Get a thirdparty

Retrieve detailed information about a specific thirdparty.

```
GET /thirdparties/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the thirdparty |

### Permissions Required

- `societe->lire` (read thirdparty permission)

### Response

Returns a thirdparty object with all fields including contact information, professional IDs, and configuration.

```json
{
  "id": 1,
  "name": "ACME Corporation",
  "name_alias": "ACME",
  "email": "contact@acme.com",
  "phone": "+1234567890",
  "address": "123 Business Street",
  "zip": "12345",
  "town": "New York",
  "country_id": 1,
  "country_code": "US",
  "client": 1,
  "fournisseur": 0,
  "code_client": "CU001",
  "tva_intra": "FR12345678901",
  "note_public": "Important customer",
  "note_private": "VIP - handle with care"
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or access not allowed |
| 404 | Thirdparty not found |

---

## Get thirdparty by email

Retrieve thirdparty information by email address.

```
GET /thirdparties/email/{email}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `email` | string | path | Yes | Email address of the thirdparty |

### Permissions Required

- `societe->lire` (read thirdparty permission)

### Response

Returns a thirdparty object matching the email address.

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/email/contact@acme.com' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Thirdparty not found |

---

## Get thirdparty by barcode

Retrieve thirdparty information by barcode.

```
GET /thirdparties/barcode/{barcode}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `barcode` | string | path | Yes | Barcode of the thirdparty |

### Permissions Required

- `societe->lire` (read thirdparty permission)

### Response

Returns a thirdparty object matching the barcode.

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/barcode/1234567890' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Thirdparty not found |

---

## List thirdparties

Retrieve a list of thirdparties with optional filtering and pagination.

```
GET /thirdparties
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `sortfield` | string | query | No | `t.rowid` | Field to sort by |
| `sortorder` | string | query | No | `ASC` | Sort order (`ASC` or `DESC`) |
| `limit` | integer | query | No | 100 | Maximum number of thirdparties to return |
| `page` | integer | query | No | 0 | Page number (0-indexed) |
| `mode` | integer | query | No | 0 | Filter by type: 1=customers only, 2=prospects only, 3=neither customer nor prospect, 4=suppliers only |
| `category` | integer | query | No | 0 | Filter by category ID |
| `sqlfilters` | string | query | No | - | Additional SQL filters |

### SQL Filters Syntax

Use the `sqlfilters` parameter to apply custom filters:

```
((t.nom:like:'ACME%') or (t.name_alias:like:'ACME%')) and (t.datec:<:'20160101')
```

Operators: `like`, `=`, `<`, `>`, `<=`, `>=`, `!=`

### Permissions Required

- `societe->lire` (read thirdparty permission)

### Response

Returns an array of thirdparty objects:

```json
[
  {
    "id": 1,
    "name": "ACME Corporation",
    "email": "contact@acme.com",
    "client": 1,
    "fournisseur": 0
  },
  {
    "id": 2,
    "name": "Tech Solutions Inc",
    "email": "info@techsolutions.com",
    "client": 3,
    "fournisseur": 1
  }
]
```

### Example Requests

**Basic list:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter customers only:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties?mode=1&limit=50' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter suppliers only:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties?mode=4' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With SQL filters:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties?sqlfilters=(t.nom:like:%27ACME%25%27)' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter by category:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties?category=5&mode=1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | No thirdparties found |
| 503 | Error when retrieving thirdparties or invalid SQL filters |

---

## Create a thirdparty

Create a new thirdparty (customer, supplier, or prospect).

```
POST /thirdparties
```

### Permissions Required

- `societe->creer` (create thirdparty permission)

### Request Body

Required fields are marked with *

```json
{
  "name": "New Company Inc",           // * Company name (required)
  "email": "contact@newcompany.com",   // * Required if SOCIETE_EMAIL_MANDATORY is enabled
  "name_alias": "NewCo",
  "address": "456 Commerce Ave",
  "zip": "54321",
  "town": "San Francisco",
  "state_id": 5,
  "country_id": 1,
  "phone": "+1987654321",
  "fax": "+1987654322",
  "url": "https://www.newcompany.com",
  "client": 1,                         // 0=not a customer, 1=customer, 2=prospect, 3=customer and prospect
  "fournisseur": 0,                    // 0=not a supplier, 1=supplier
  "code_client": "CU002",
  "code_fournisseur": "",
  "code_compta": "411200",
  "tva_intra": "FR98765432109",
  "idprof1": "123456789",              // SIREN (France) or equivalent
  "idprof2": "12345678900001",         // SIRET (France) or equivalent
  "idprof3": "1234Z",                  // APE/NAF (France) or equivalent
  "note_public": "Key account",
  "note_private": "Contact: John Doe"
}
```

### Response

Returns the ID of the created thirdparty:

```json
2
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/thirdparties' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "New Company Inc",
    "email": "contact@newcompany.com",
    "client": 1,
    "address": "456 Commerce Ave",
    "zip": "54321",
    "town": "San Francisco",
    "country_id": 1
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Missing required field (name or email if mandatory) |
| 401 | Insufficient rights |
| 500 | Error creating thirdparty |

---

## Update a thirdparty

Update an existing thirdparty's information.

```
PUT /thirdparties/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the thirdparty to update |

### Permissions Required

- `societe->creer` (create/modify thirdparty permission)

### Request Body

Send only the fields you want to update:

```json
{
  "name": "ACME Corporation Ltd",
  "email": "newcontact@acme.com",
  "phone": "+1234567899",
  "note_public": "Updated information"
}
```

### Response

Returns the updated thirdparty object.

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/thirdparties/1' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "phone": "+1234567899",
    "email": "newcontact@acme.com"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Thirdparty not found |
| 500 | Error updating thirdparty |

---

## Merge thirdparties

Merge a thirdparty into another one. This operation merges content (properties, notes) and objects (invoices, events, orders, proposals, etc.) from one thirdparty into a target thirdparty, then deletes the merged thirdparty.

```
PUT /thirdparties/{id}/merge/{idtodelete}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty to keep (target) |
| `idtodelete` | integer | path | Yes | ID of thirdparty to remove (will be merged into target) |

### Permissions Required

- `societe->creer` (create/modify thirdparty permission)

### Behavior

- Properties with defined values in both thirdparties: target thirdparty values are kept
- Notes: content is concatenated
- Categories: merged from both thirdparties
- All related objects (invoices, orders, etc.) are transferred to the target thirdparty
- Extra fields are merged (target values take precedence)
- The source thirdparty is deleted after merge

### Response

Returns the updated target thirdparty object after merge.

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/merge/5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Trying to merge a thirdparty into itself |
| 401 | User doesn't have permission |
| 404 | One or both thirdparties not found |
| 500 | Error during merge operation |

---

## Delete a thirdparty

Delete a thirdparty from the system.

```
DELETE /thirdparties/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the thirdparty to delete |

### Permissions Required

- `societe->supprimer` (delete thirdparty permission)

### Response

```json
{
  "success": {
    "code": 200,
    "message": "Object deleted"
  }
}
```

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/thirdparties/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Thirdparty not found |
| 409 | Can't delete, thirdparty is probably being used |
| 500 | Error deleting thirdparty |

---

## Set price level

Set a new price level for a thirdparty (requires multiprices feature enabled).

```
PUT /thirdparties/{id}/setpricelevel
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty |
| `priceLevel` | integer | body | Yes | Price level (1 to PRODUIT_MULTIPRICES_LIMIT) |

### Permissions Required

- `societe->creer` (create/modify thirdparty permission)
- Module "Thirdparties" enabled
- Module "Products" enabled
- Setting "PRODUIT_MULTIPRICES" enabled

### Request Body

```json
{
  "priceLevel": 2
}
```

### Response

Returns the updated thirdparty object.

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/setpricelevel' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "priceLevel": 2
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Price level out of bounds |
| 401 | User doesn't have permission |
| 404 | Thirdparty not found |
| 500 | Error setting price level |
| 501 | Required modules or settings not enabled |

---

## Customer Categories

### Get customer categories

Retrieve all customer categories assigned to a thirdparty.

```
GET /thirdparties/{id}/categories
```

#### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of thirdparty |
| `sortfield` | string | query | No | `s.rowid` | Field to sort by |
| `sortorder` | string | query | No | `ASC` | Sort order |
| `limit` | integer | query | No | 0 | Limit for list |
| `page` | integer | query | No | 0 | Page number |

#### Permissions Required

- `categorie->lire` (read category permission)

#### Response

Returns an array of category objects.

#### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/categories' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Add customer category

Add a customer category to a thirdparty.

```
POST /thirdparties/{id}/categories/{category_id}
```

#### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty |
| `category_id` | integer | path | Yes | ID of category to add |

#### Permissions Required

- `societe->creer` (create/modify thirdparty permission)

#### Response

Returns the updated thirdparty object.

#### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/categories/5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Remove customer category

Remove a customer category from a thirdparty.

```
DELETE /thirdparties/{id}/categories/{category_id}
```

#### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty |
| `category_id` | integer | path | Yes | ID of category to remove |

#### Permissions Required

- `societe->creer` (create/modify thirdparty permission)

#### Response

Returns the updated thirdparty object.

#### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/categories/5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Supplier Categories

### Get supplier categories

Retrieve all supplier categories assigned to a thirdparty.

```
GET /thirdparties/{id}/supplier_categories
```

#### Parameters

Same as customer categories endpoint.

#### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/supplier_categories' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Add supplier category

Add a supplier category to a thirdparty.

```
POST /thirdparties/{id}/supplier_categories/{category_id}
```

#### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/supplier_categories/8' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Remove supplier category

Remove a supplier category from a thirdparty.

```
DELETE /thirdparties/{id}/supplier_categories/{category_id}
```

#### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/supplier_categories/8' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Outstanding Documents

### Get outstanding proposals

Retrieve outstanding proposals for a thirdparty.

```
GET /thirdparties/{id}/outstandingproposals
```

#### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of thirdparty |
| `mode` | string | query | No | `customer` | Mode: 'customer' or 'supplier' |

#### Permissions Required

- `societe->lire` (read thirdparty permission)

#### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/outstandingproposals?mode=customer' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Get outstanding orders

Retrieve outstanding orders for a thirdparty.

```
GET /thirdparties/{id}/outstandingorders
```

#### Parameters

Same as outstanding proposals.

#### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/outstandingorders' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Get outstanding invoices

Retrieve outstanding invoices for a thirdparty.

```
GET /thirdparties/{id}/outstandinginvoices
```

#### Parameters

Same as outstanding proposals.

#### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/outstandinginvoices' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Sales Representatives

Get sales representatives assigned to a thirdparty.

```
GET /thirdparties/{id}/representatives
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of thirdparty |
| `mode` | integer | query | No | 0 | 0=Array with properties, 1=Array of IDs only |

### Permissions Required

- `societe->lire` (read thirdparty permission)

### Response

```json
[
  {
    "id": 3,
    "firstname": "John",
    "lastname": "Sales",
    "email": "john.sales@company.com"
  }
]
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/representatives' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Fixed Amount Discounts

Get fixed amount discounts for a thirdparty (from deposits, credit notes, commercial offers, etc.).

```
GET /thirdparties/{id}/fixedamountdiscounts
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of thirdparty |
| `filter` | string | query | No | `none` | Filter: 'none'=all, 'available'=unapplied, 'used'=applied |
| `sortfield` | string | query | No | `f.type` | Field to sort by |
| `sortorder` | string | query | No | `ASC` | Sort order |

### Permissions Required

- `societe->lire` (read thirdparty permission)

### Response

```json
[
  {
    "ref": "FA2024-001",
    "factype": 2,
    "fk_facture_source": 15,
    "rowid": 1,
    "amount_ht": 100.00,
    "amount_tva": 20.00,
    "amount_ttc": 120.00,
    "description": "Credit note discount",
    "fk_facture": null,
    "fk_facture_line": null
  }
]
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/fixedamountdiscounts?filter=available' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Invoices for Replacement/Credit Note

### Get invoices qualified for replacement

Get list of invoices that can be replaced by another invoice.

```
GET /thirdparties/{id}/getinvoicesqualifiedforreplacement
```

#### Permissions Required

- `facture->lire` (read invoice permission)

#### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/getinvoicesqualifiedforreplacement' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Get invoices qualified for credit note

Get list of invoices that can be corrected by a credit note.

```
GET /thirdparties/{id}/getinvoicesqualifiedforcreditnote
```

#### Permissions Required

- `facture->lire` (read invoice permission)

#### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/getinvoicesqualifiedforcreditnote' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Bank Accounts

### Get bank accounts

Retrieve all bank accounts for a thirdparty.

```
GET /thirdparties/{id}/bankaccounts
```

#### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty |

#### Permissions Required

- `societe->lire` (read thirdparty permission)

#### Response

```json
[
  {
    "id": 1,
    "socid": 1,
    "default_rib": 1,
    "label": "Main account",
    "bank": "BNP Paribas",
    "bic": "BNPAFRPPXXX",
    "iban": "FR7630004000031234567890143",
    "rum": "RUM-CU001-001",
    "frstrecur": "FRST",
    "datec": 1704067200,
    "datem": 1706745600
  }
]
```

#### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/bankaccounts' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Create bank account

Create a new bank account for a thirdparty.

```
POST /thirdparties/{id}/bankaccounts
```

#### Permissions Required

- `societe->creer` (create/modify thirdparty permission)

#### Request Body

```json
{
  "label": "Secondary account",
  "bank": "Crédit Agricole",
  "bic": "AGRIFRPPXXX",
  "iban": "FR7612345678901234567890123",
  "default_rib": 0
}
```

#### Response

Returns the created bank account object.

#### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/bankaccounts' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "label": "Secondary account",
    "iban": "FR7612345678901234567890123",
    "bic": "AGRIFRPPXXX"
  }'
```

### Update bank account

Update a bank account for a thirdparty.

```
PUT /thirdparties/{id}/bankaccounts/{bankaccount_id}
```

#### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty |
| `bankaccount_id` | integer | path | Yes | ID of bank account |

#### Request Body

Send only fields to update:

```json
{
  "label": "Updated account label",
  "default_rib": 1
}
```

#### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/bankaccounts/1' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "default_rib": 1
  }'
```

### Delete bank account

Delete a bank account from a thirdparty.

```
DELETE /thirdparties/{id}/bankaccounts/{bankaccount_id}
```

#### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty |
| `bankaccount_id` | integer | path | Yes | ID of bank account |

#### Permissions Required

- `societe->creer` (create/modify thirdparty permission)

#### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/bankaccounts/2' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Generate bank account document

Generate a document (like SEPA mandate) from a bank account record.

```
GET /thirdparties/{id}/generateBankAccountDocument/{companybankid}/{model}
```

#### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of thirdparty |
| `companybankid` | integer | path | No | null | ID of bank account (null for all) |
| `model` | string | path | No | `sepamandate` | Document model |

#### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/generateBankAccountDocument/1/sepamandate' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Gateway Accounts

Gateway accounts (also called "Societe Accounts") are used to store third-party payment gateway credentials and references (e.g., Stripe customer IDs, PayPal accounts).

### Get gateway accounts

Retrieve gateway accounts for a thirdparty, optionally filtered by site.

```
GET /thirdparties/{id}/gateways
```

#### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty |
| `site` | string | query | No | Filter by site key (e.g., 'stripe', 'paypal') |

#### Permissions Required

- `societe->lire` (read thirdparty permission)

#### Response

```json
[
  {
    "id": 1,
    "fk_soc": 1,
    "key_account": "cus_ABC123XYZ",
    "site": "stripe",
    "date_creation": 1704067200,
    "tms": 1706745600
  }
]
```

#### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/gateways?site=stripe' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Create gateway account

Create a new gateway account for a thirdparty.

```
POST /thirdparties/{id}/gateways
```

#### Permissions Required

- `societe->creer` (create/modify thirdparty permission)

#### Request Body

```json
{
  "key_account": "cus_ABC123XYZ",
  "site": "stripe",
  "login": "customer@email.com"
}
```

#### Response

Returns the created gateway account object.

#### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/gateways' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "key_account": "cus_ABC123XYZ",
    "site": "stripe"
  }'
```

#### Error Responses

| Status Code | Description |
|-------------|-------------|
| 409 | Gateway account already exists for this company and site |
| 422 | Missing required field 'site' |
| 500 | Error creating gateway account |

### Update/Replace gateway account

Create or completely replace a gateway account for a specific site.

```
PUT /thirdparties/{id}/gateways/{site}
```

**Warning:** This replaces ALL values. Use PATCH to update specific fields only.

#### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty |
| `site` | string | path | Yes | Site key |

#### Request Body

```json
{
  "key_account": "cus_NEW123XYZ",
  "login": "newemail@company.com"
}
```

#### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/gateways/stripe' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "key_account": "cus_NEW123XYZ"
  }'
```

### Partially update gateway account

Update specific fields of a gateway account.

```
PATCH /thirdparties/{id}/gateways/{site}
```

#### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty |
| `site` | string | path | Yes | Site key |

#### Request Body

Send only fields to update:

```json
{
  "key_account": "cus_UPDATED123"
}
```

#### Example Request

```bash
curl -X PATCH \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/gateways/stripe' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "key_account": "cus_UPDATED123"
  }'
```

### Delete specific gateway account

Delete a gateway account by site.

```
DELETE /thirdparties/{id}/gateways/{site}
```

#### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of thirdparty |
| `site` | string | path | Yes | Site key |

#### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/gateways/stripe' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Delete all gateway accounts

Delete all gateway accounts for a thirdparty.

```
DELETE /thirdparties/{id}/gateways
```

#### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/thirdparties/1/gateways' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Thirdparty Object

### Client/Supplier Type Values

The `client` field indicates the thirdparty type:

| Value | Description |
|-------|-------------|
| 0 | Not a customer/prospect |
| 1 | Customer |
| 2 | Prospect |
| 3 | Customer and prospect |

The `fournisseur` field:

| Value | Description |
|-------|-------------|
| 0 | Not a supplier |
| 1 | Supplier |

### Professional ID Fields

Professional ID fields vary by country:

**France:**
- `idprof1` = SIREN
- `idprof2` = SIRET
- `idprof3` = APE/NAF code
- `idprof4` = RCS

**Other countries:** Check Dolibarr documentation for your country's professional ID mapping.

---

## Notes

- External users can only access thirdparties linked to their account
- Internal users can only see thirdparties they manage, unless they have "See all" permission
- The `name` field is required when creating a thirdparty
- If `SOCIETE_EMAIL_MANDATORY` is enabled, the `email` field is also required
- The `id` field cannot be modified when updating
- Some fields are automatically cleaned from responses for security reasons
- When merging thirdparties, the operation is transactional and will rollback on error
- Bank account RUM numbers are automatically generated if not provided
- Gateway accounts must have unique site keys per thirdparty

---

## See Also

- [Thirdparty Fields Reference](./thirdparties/api_fields_thirdparty.md) - Complete list of API fields
- [Contacts API](./contacts.md) - Manage contacts linked to thirdparties
- [Invoices API](./invoices.md) - Manage invoices for thirdparties
- [Orders API](./orders.md) - Manage orders for thirdparties
