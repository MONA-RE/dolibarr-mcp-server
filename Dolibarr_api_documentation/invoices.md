# Invoices API

The Invoices API allows you to manage customer invoices in your Dolibarr instance. You can create, read, update, delete invoices, manage invoice lines, handle payments, and work with discounts and credit notes.

## Endpoints

### Invoice Management
- [Get an invoice](#get-an-invoice)
- [Get invoice by reference](#get-invoice-by-reference)
- [Get invoice by external reference](#get-invoice-by-external-reference)
- [List invoices](#list-invoices)
- [Create an invoice](#create-an-invoice)
- [Create invoice from order](#create-invoice-from-order)
- [Update an invoice](#update-an-invoice)
- [Delete an invoice](#delete-an-invoice)

### Invoice Status
- [Validate an invoice](#validate-an-invoice)
- [Set invoice to draft](#set-invoice-to-draft)
- [Set invoice to paid](#set-invoice-to-paid)
- [Set invoice to unpaid](#set-invoice-to-unpaid)

### Invoice Lines
- [Get invoice lines](#get-invoice-lines)
- [Add a line to invoice](#add-a-line-to-invoice)
- [Update an invoice line](#update-an-invoice-line)
- [Delete an invoice line](#delete-an-invoice-line)

### Contacts
- [Add contact to invoice](#add-contact-to-invoice)
- [Add contact (alternative)](#add-contact-alternative)
- [Delete contact from invoice](#delete-contact-from-invoice)

### Payments
- [Get invoice payments](#get-invoice-payments)
- [Add payment to invoice](#add-payment-to-invoice)
- [Add distributed payment](#add-distributed-payment)
- [Update a payment](#update-a-payment)

### Discounts and Credit Notes
- [Get discount from invoice](#get-discount-from-invoice)
- [Use discount on invoice](#use-discount-on-invoice)
- [Use credit note on invoice](#use-credit-note-on-invoice)
- [Mark as credit available](#mark-as-credit-available)

### Template Invoices
- [Get template invoice](#get-template-invoice)

---

## Get an invoice

Retrieve detailed information about a specific invoice by ID.

```
GET /invoices/{id}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the invoice |
| `contact_list` | integer | query | No | 1 | Contact detail level: 0=All properties, 1=Just IDs, -1=No contacts |

### Permissions Required

- `facture->lire` (read invoice permission)

### Response

Returns an invoice object with payment details calculated:

```json
{
  "id": 1,
  "ref": "FA2401-0001",
  "socid": 5,
  "date": 1704067200,
  "date_lim_reglement": 1706745600,
  "type": 0,
  "total_ht": 1000.00,
  "total_tva": 200.00,
  "total_ttc": 1200.00,
  "totalpaid": 500.00,
  "totalcreditnotes": 0,
  "totaldeposits": 0,
  "remaintopay": 700.00,
  "paye": 0,
  "statut": 1,
  "fk_statut": 1,
  "lines": [],
  "contacts_ids": []
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or access not allowed |
| 404 | Invoice not found |

---

## Get invoice by reference

Retrieve an invoice using its reference number.

```
GET /invoices/ref/{ref}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `ref` | string | path | Yes | - | Reference of the invoice |
| `contact_list` | integer | query | No | 1 | Contact detail level: 0=All properties, 1=Just IDs, -1=No contacts |

### Permissions Required

- `facture->lire` (read invoice permission)

### Response

Returns the same invoice object as [Get an invoice](#get-an-invoice).

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices/ref/FA2401-0001' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Invoice not found |

---

## Get invoice by external reference

Retrieve an invoice using its external reference.

```
GET /invoices/ref_ext/{ref_ext}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `ref_ext` | string | path | Yes | - | External reference of the invoice |
| `contact_list` | integer | query | No | 1 | Contact detail level: 0=All properties, 1=Just IDs, -1=No contacts |

### Permissions Required

- `facture->lire` (read invoice permission)

### Response

Returns the same invoice object as [Get an invoice](#get-an-invoice).

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices/ref_ext/EXT-INV-2024-001' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Invoice not found |

---

## List invoices

Retrieve a list of invoices with optional filtering and pagination.

```
GET /invoices
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `sortfield` | string | query | No | `t.rowid` | Field to sort by |
| `sortorder` | string | query | No | `ASC` | Sort order (`ASC` or `DESC`) |
| `limit` | integer | query | No | 100 | Maximum number of invoices to return |
| `page` | integer | query | No | 0 | Page number (0-indexed) |
| `thirdparty_ids` | string | query | No | - | Filter by third party IDs (comma-separated, e.g., '1,2,3') |
| `status` | string | query | No | - | Filter by status: `draft`, `unpaid`, `paid`, `cancelled` |
| `sqlfilters` | string | query | No | - | Additional SQL filters |

### SQL Filters Syntax

Use the `sqlfilters` parameter to apply custom filters:

```
(t.ref:like:'FA%') and (t.date_creation:<:'20240101')
```

Operators: `like`, `=`, `<`, `>`, `<=`, `>=`, `!=`

### Permissions Required

- `facture->lire` (read invoice permission)

### Response

Returns an array of invoice objects with payment calculations:

```json
[
  {
    "id": 1,
    "ref": "FA2401-0001",
    "socid": 5,
    "date": 1704067200,
    "total_ttc": 1200.00,
    "totalpaid": 500.00,
    "remaintopay": 700.00,
    "statut": 1,
    "contacts_ids": []
  },
  {
    "id": 2,
    "ref": "FA2401-0002",
    "socid": 8,
    "total_ttc": 850.00,
    "remaintopay": 0,
    "statut": 2
  }
]
```

### Example Requests

**Basic list:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter by status:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices?status=unpaid' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter by third party:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices?thirdparty_ids=5,8' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With SQL filters:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices?sqlfilters=(t.ref:like:%27FA2401%25%27)' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Status Filter Values

| Value | Description | Database Status |
|-------|-------------|-----------------|
| `draft` | Draft invoices | `fk_statut = 0` |
| `unpaid` | Validated but unpaid | `fk_statut = 1` |
| `paid` | Paid invoices | `fk_statut = 2` |
| `cancelled` | Cancelled invoices | `fk_statut = 3` |

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | No invoices found |
| 503 | Error when retrieving invoice list or invalid sqlfilters |

---

## Create an invoice

Create a new customer invoice.

```
POST /invoices
```

### Permissions Required

- `facture->creer` (create invoice permission)

### Request Body

Required fields are marked with *

```json
{
  "socid": 5,                    // * Third party ID (required)
  "date": 1704067200,            // Invoice date (Unix timestamp) - defaults to current date
  "date_lim_reglement": 1706745600,  // Payment due date (Unix timestamp)
  "type": 0,                     // Invoice type (see types below)
  "cond_reglement_id": 1,        // Payment term ID
  "mode_reglement_id": 1,        // Payment mode ID
  "note_private": "Internal note",
  "note_public": "Public note visible to customer",
  "fk_account": 1,               // Bank account ID
  "lines": [                     // Invoice lines (see Add a line format)
    {
      "fk_product": 1,
      "qty": 2,
      "subprice": 100.00,
      "tva_tx": 20.000
    }
  ]
}
```

### Invoice Types

| Value | Description |
|-------|-------------|
| 0 | Standard invoice (TYPE_STANDARD) |
| 1 | Replacement invoice (TYPE_REPLACEMENT) |
| 2 | Credit note (TYPE_CREDIT_NOTE) |
| 3 | Deposit invoice (TYPE_DEPOSIT) |
| 4 | Situation invoice (TYPE_SITUATION) |

### Response

Returns the ID of the created invoice:

```json
3
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "socid": 5,
    "date": 1704067200,
    "date_lim_reglement": 1706745600,
    "type": 0,
    "note_public": "Invoice for January services"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Missing required field (socid) |
| 401 | Insufficient rights |
| 500 | Error creating invoice |

---

## Create invoice from order

Create an invoice based on an existing order.

```
POST /invoices/createfromorder/{orderid}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `orderid` | integer | path | Yes | ID of the order to invoice |

### Permissions Required

- `commande->lire` (read order permission)
- `facture->creer` (create invoice permission)

### Response

Returns the complete invoice object created from the order.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/createfromorder/15' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Order ID is mandatory |
| 401 | User doesn't have permission |
| 404 | Order not found |
| 405 | Error creating invoice from order |

---

## Update an invoice

Update an existing invoice's fields.

```
PUT /invoices/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the invoice to update |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Request Body

Send only the fields you want to update:

```json
{
  "note_public": "Updated public note",
  "note_private": "Updated private note",
  "date_lim_reglement": 1709424000,
  "fk_account": 2
}
```

**Note:** When updating `fk_account`, the bank account is automatically set using the `setBankAccount()` method.

### Response

Returns the updated invoice object.

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/invoices/1' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "note_public": "Updated payment terms",
    "date_lim_reglement": 1709424000
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Error setting bank account |
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 500 | Error updating invoice |

---

## Delete an invoice

Delete an invoice from the system.

```
DELETE /invoices/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the invoice to delete |

### Permissions Required

- `facture->supprimer` (delete invoice permission)

### Response

```json
{
  "success": {
    "code": 200,
    "message": "Invoice deleted"
  }
}
```

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/invoices/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 500 | Error when deleting invoice |

---

## Validate an invoice

Validate a draft invoice (changes status from draft to validated).

```
POST /invoices/{id}/validate
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the invoice |
| `idwarehouse` | integer | body | No | 0 | Warehouse ID for stock management |
| `notrigger` | integer | body | No | 0 | 1=Don't execute triggers, 0=Execute triggers |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Request Body

```json
{
  "idwarehouse": 0,
  "notrigger": 0
}
```

### Response

Returns the validated invoice object.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/validate' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "idwarehouse": 0,
    "notrigger": 0
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 304 | Nothing done - invoice may already be validated |
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 500 | Error when validating invoice |

---

## Set invoice to draft

Set a validated invoice back to draft status.

```
POST /invoices/{id}/settodraft
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the invoice |
| `idwarehouse` | integer | body | No | -1 | Warehouse ID for stock reintegration |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Request Body

```json
{
  "idwarehouse": -1
}
```

### Response

Returns the invoice object now in draft status.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/settodraft' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 304 | Nothing done |
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 500 | Error setting invoice to draft |

---

## Set invoice to paid

Mark an invoice as paid (even if payment amount doesn't match total).

```
POST /invoices/{id}/settopaid
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the invoice |
| `close_code` | string | body | No | '' | Code when classifying as paid with incomplete payment |
| `close_note` | string | body | No | '' | Comment when classifying as paid with incomplete payment |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Request Body

```json
{
  "close_code": "discount",
  "close_note": "Discount applied for early payment"
}
```

### Response

Returns the invoice object with paid status.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/settopaid' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "close_code": "discount",
    "close_note": "Early payment discount"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 304 | Nothing done - may already be paid |
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 500 | Error setting invoice to paid |

---

## Set invoice to unpaid

Mark a paid invoice as unpaid.

```
POST /invoices/{id}/settounpaid
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the invoice |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Response

Returns the invoice object with unpaid status.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/settounpaid' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 304 | Nothing done |
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 500 | Error setting invoice to unpaid |

---

## Get invoice lines

Retrieve all lines (items) from a specific invoice.

```
GET /invoices/{id}/lines
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the invoice |

### Permissions Required

- `facture->lire` (read invoice permission)

### Response

Returns an array of invoice line objects:

```json
[
  {
    "id": 10,
    "fk_facture": 1,
    "fk_product": 15,
    "description": "Web development services",
    "qty": 10,
    "subprice": 100.00,
    "tva_tx": 20.000,
    "total_ht": 1000.00,
    "total_tva": 200.00,
    "total_ttc": 1200.00,
    "product_type": 1,
    "rang": 1
  }
]
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices/1/lines' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Invoice not found |

---

## Add a line to invoice

Add a new line (item) to an existing invoice.

```
POST /invoices/{id}/lines
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the invoice |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Request Body

Example of complete line data:

```json
{
  "desc": "Product or service description",
  "subprice": 100.00,
  "qty": 1,
  "tva_tx": 20.000,
  "localtax1_tx": 0.000,
  "localtax2_tx": 0.000,
  "fk_product": 1,
  "remise_percent": 0,
  "date_start": "",
  "date_end": "",
  "fk_code_ventilation": 0,
  "info_bits": 0,
  "fk_remise_except": null,
  "product_type": 1,
  "rang": -1,
  "special_code": 0,
  "fk_parent_line": null,
  "fk_fournprice": null,
  "pa_ht": 0,
  "label": "",
  "array_options": [],
  "situation_percent": 100,
  "fk_prev_id": null,
  "fk_unit": null,
  "ref_ext": "",
  "price_base_type": "HT"
}
```

### Common Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `desc` | string | Yes | Line description (HTML restricted) |
| `qty` | float | Yes | Quantity |
| `subprice` | float | Yes | Unit price excluding tax |
| `tva_tx` | float | Yes | VAT rate (e.g., 20.000 for 20%) |
| `fk_product` | integer | No | Product/Service ID |
| `remise_percent` | float | No | Discount percentage |
| `product_type` | integer | No | 0=Product, 1=Service, 9=Special |
| `label` | string | No | Short label |
| `date_start` | timestamp | No | Start date for services |
| `date_end` | timestamp | No | End date for services |

### Response

Returns the ID of the created line:

```json
25
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/lines' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "desc": "Consulting services - January 2024",
    "subprice": 150.00,
    "qty": 8,
    "tva_tx": 20.000,
    "product_type": 1,
    "label": "Consulting"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Unable to insert line - check inputs |
| 401 | User doesn't have permission |
| 404 | Invoice not found |

---

## Update an invoice line

Update an existing line in an invoice.

```
PUT /invoices/{id}/lines/{lineid}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the invoice |
| `lineid` | integer | path | Yes | ID of the line to update |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Request Body

Send the fields to update (same format as adding a line):

```json
{
  "desc": "Updated description",
  "subprice": 120.00,
  "qty": 5,
  "tva_tx": 20.000,
  "remise_percent": 10
}
```

### Response

Returns the updated invoice object (without the `line` property).

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/invoices/1/lines/25' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "qty": 10,
    "subprice": 125.00
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 304 | Error updating line |
| 401 | User doesn't have permission |
| 404 | Invoice not found |

---

## Delete an invoice line

Remove a line from an invoice.

```
DELETE /invoices/{id}/lines/{lineid}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the invoice |
| `lineid` | integer | path | Yes | ID of the line to delete |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Response

Returns the updated invoice object.

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/invoices/1/lines/25' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Line ID is mandatory |
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 405 | Error deleting line |

---

## Add contact to invoice

Add a contact relationship to an invoice using contact type code.

```
POST /invoices/{id}/contact/{contactid}/{type}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the invoice |
| `contactid` | integer | path | Yes | ID of the contact |
| `type` | string | path | Yes | Contact type: `BILLING`, `SHIPPING`, or `CUSTOMER` |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Response

Returns the updated invoice object.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/contact/5/BILLING' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 500 | Invalid type or error when adding contact |

---

## Add contact (alternative)

Add a contact to an invoice with full control over contact source and type.

```
POST /invoices/{id}/contacts
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | Invoice ID |
| `fk_socpeople` | integer | body | Yes | - | Contact ID (if external) or User ID (if internal) |
| `type_contact` | string | body | Yes | - | Contact type code (e.g., 'BILLING') |
| `source` | string | body | Yes | - | 'external' or 'internal' |
| `notrigger` | integer | body | No | 0 | 1=Disable triggers, 0=Execute triggers |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Request Body

```json
{
  "fk_socpeople": 5,
  "type_contact": "BILLING",
  "source": "external",
  "notrigger": 0
}
```

### Response

Returns the updated invoice object.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/contacts' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "fk_socpeople": 5,
    "type_contact": "BILLING",
    "source": "external"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 304 | Error adding contact |
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 500 | Error adding contact |

---

## Delete contact from invoice

Remove a contact relationship from an invoice.

```
DELETE /invoices/{id}/contact/{contactid}/{type}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the invoice |
| `contactid` | integer | path | Yes | Row key of contact in contact_ids array |
| `type` | string | path | Yes | Contact type: `BILLING`, `SHIPPING`, or `CUSTOMER` |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Response

Returns the updated invoice object.

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/invoices/1/contact/5/BILLING' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 500 | Error when deleting contact |

---

## Get invoice payments

Retrieve list of all payments associated with an invoice.

```
GET /invoices/{id}/payments
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the invoice |

### Permissions Required

- `facture->lire` (read invoice permission)

### Response

Returns an array of payment records:

```json
[
  {
    "date": 1704153600,
    "amount": 500.00,
    "type": "VIR",
    "num": "PAYMENT-001"
  }
]
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices/1/payments' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Invoice ID is mandatory |
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 405 | Error retrieving payments |

---

## Add payment to invoice

Add a payment for the remaining amount due on an invoice.

```
POST /invoices/{id}/payments
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | Invoice ID |
| `datepaye` | timestamp | body | Yes | Payment date (Unix timestamp) |
| `paymentid` | integer | body | Yes | Payment mode ID |
| `closepaidinvoices` | string | body | Yes | Close paid invoices: `yes` or `no` |
| `accountid` | integer | body | Yes* | Bank account ID (*required if banking module enabled) |
| `num_payment` | string | body | No | Payment number (optional) |
| `comment` | string | body | No | Private note (optional) |
| `chqemetteur` | string | body | No* | Check issuer (*mandatory if payment type is CHQ) |
| `chqbank` | string | body | No | Issuer bank name (optional) |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Request Body

```json
{
  "datepaye": 1704153600,
  "paymentid": 4,
  "closepaidinvoices": "yes",
  "accountid": 1,
  "num_payment": "PAY-2024-001",
  "comment": "Payment received by bank transfer"
}
```

### Response

Returns the ID of the created payment:

```json
15
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/payments' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "datepaye": 1704153600,
    "paymentid": 4,
    "closepaidinvoices": "yes",
    "accountid": 1,
    "comment": "Bank transfer payment"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Missing required parameter or check issuer required |
| 403 | User doesn't have permission |
| 404 | Invoice not found |

---

## Add distributed payment

Add a payment distributed across multiple invoices.

```
POST /invoices/paymentsdistributed
```

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Request Body

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `arrayofamounts` | object | Yes | Object with invoice IDs as keys and amount objects as values |
| `datepaye` | timestamp | Yes | Payment date (Unix timestamp) |
| `paymentid` | integer | Yes | Payment mode ID |
| `closepaidinvoices` | string | Yes | Close paid invoices: `yes` or `no` |
| `accountid` | integer | Yes* | Bank account ID (*required if banking enabled) |
| `num_payment` | string | No | Payment number (optional) |
| `comment` | string | No | Private note (optional) |
| `chqemetteur` | string | No* | Check issuer (*mandatory if payment type is CHQ) |
| `chqbank` | string | No | Issuer bank name (optional) |
| `ref_ext` | string | No | External reference (optional) |
| `accepthigherpayment` | boolean | No | Accept higher payments than remain to pay (optional) |

### Amount Object Format

For each invoice in `arrayofamounts`:

```json
{
  "1": {
    "amount": "99.99",              // Amount in default currency
    "multicurrency_amount": ""       // Amount in invoice currency (alternative)
  },
  "2": {
    "amount": "remain",              // Special value: pay all remaining
    "multicurrency_amount": ""
  },
  "3": {
    "amount": "",
    "multicurrency_amount": "150.00" // Use invoice's multicurrency
  }
}
```

**Note:** Only specify `amount` OR `multicurrency_amount`, not both. Use `"remain"` to pay the full remaining balance.

### Complete Request Example

```json
{
  "arrayofamounts": {
    "1": {
      "amount": "500.00",
      "multicurrency_amount": ""
    },
    "2": {
      "amount": "remain",
      "multicurrency_amount": ""
    }
  },
  "datepaye": 1704153600,
  "paymentid": 4,
  "closepaidinvoices": "yes",
  "accountid": 1,
  "num_payment": "BATCH-PAY-001",
  "comment": "Batch payment for multiple invoices"
}
```

### Response

Returns the ID of the created payment:

```json
20
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/paymentsdistributed' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "arrayofamounts": {
      "1": {"amount": "500.00", "multicurrency_amount": ""},
      "2": {"amount": "300.00", "multicurrency_amount": ""}
    },
    "datepaye": 1704153600,
    "paymentid": 4,
    "closepaidinvoices": "yes",
    "accountid": 1
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Missing/invalid parameters, payment higher than remaining, both currencies specified |
| 403 | User doesn't have permission or access denied for invoice |
| 404 | Invoice not found |

---

## Update a payment

Update payment information (currently only supports updating payment number).

```
PUT /invoices/payments/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | Payment ID |
| `num_payment` | string | body | No | New payment number |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Request Body

```json
{
  "num_payment": "PAY-2024-NEW"
}
```

### Response

```json
{
  "success": {
    "code": 200,
    "message": "Payment updated"
  }
}
```

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/invoices/payments/15' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "num_payment": "PAY-2024-UPDATED"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Payment ID is mandatory |
| 401 | User doesn't have permission |
| 404 | Payment not found |
| 500 | Error when updating payment |

---

## Get discount from invoice

Get discount information created from a credit note or deposit invoice.

```
GET /invoices/{id}/discount
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | Invoice ID |

### Permissions Required

- `facture->lire` (read invoice permission)

### Response

Returns a discount object:

```json
{
  "id": 5,
  "fk_soc": 5,
  "fk_facture_source": 1,
  "amount_ht": 100.00,
  "amount_tva": 20.00,
  "amount_ttc": 120.00,
  "tva_tx": 20.000,
  "description": "(CREDIT_NOTE)"
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices/1/discount' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Invoice or discount not found |
| 500 | Error retrieving discount |

---

## Mark as credit available

Convert a credit note or deposit invoice into available credit (discount).

```
POST /invoices/{id}/markAsCreditAvailable
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | Invoice ID |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Eligible Invoices

This endpoint works for:
- **Credit notes** (type 2) that are unpaid
- **Deposit invoices** (type 3) that haven't been converted yet
- **Standard/Replacement invoices** (types 0/1) with excess payment received

### Response

Returns the updated invoice object.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/markAsCreditAvailable' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 500 | Already paid, can't convert, discount creation error, or couldn't set paid |

---

## Use discount on invoice

Apply an existing absolute discount to an invoice as a line item.

```
POST /invoices/{id}/usediscount/{discountid}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | Invoice ID |
| `discountid` | integer | path | Yes | Discount ID to consume |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Response

Returns result code (positive on success).

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/usediscount/5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Invoice ID or Discount ID is mandatory |
| 401 | User doesn't have permission |
| 404 | Invoice not found |
| 405 | Error applying discount |

**Note:** This consumes the discount and adds it as a line on the invoice.

---

## Use credit note on invoice

Apply a credit note discount to an invoice's payments (not as a line).

```
POST /invoices/{id}/usecreditnote/{discountid}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | Invoice ID |
| `discountid` | integer | path | Yes | Credit note discount ID |

### Permissions Required

- `facture->creer` (create/modify invoice permission)

### Response

Returns result code (positive on success).

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/invoices/1/usecreditnote/5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Invoice ID or Credit ID is mandatory |
| 401 | User doesn't have permission |
| 404 | Invoice or credit not found |
| 405 | Error linking credit note |

**Note:** This consumes the credit note and links it to the invoice as a payment reduction.

---

## Get template invoice

Retrieve a recurring/template invoice.

```
GET /invoices/templates/{id}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | Template invoice ID |
| `contact_list` | integer | query | No | 1 | Contact detail level: 0=All properties, 1=Just IDs, -1=No contacts |

### Permissions Required

- `facture->lire` (read invoice permission)

### Response

Returns a template invoice object (FactureRec):

```json
{
  "id": 1,
  "title": "Monthly subscription",
  "socid": 5,
  "frequency": 1,
  "unit_frequency": "m",
  "date_when": 1704067200,
  "nb_gen_done": 3,
  "nb_gen_max": 12
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/invoices/templates/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Template invoice not found |

---

## Invoice Object

### Main Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Invoice ID |
| `ref` | string | Invoice reference (e.g., FA2401-0001) |
| `ref_ext` | string | External reference |
| `socid` | integer | Third party (customer) ID |
| `type` | integer | Invoice type (0-4, see types table) |
| `date` | timestamp | Invoice date |
| `date_lim_reglement` | timestamp | Payment due date |
| `date_validation` | timestamp | Validation date |
| `paye` | integer | Paid status: 0=Unpaid, 1=Paid |
| `statut` / `fk_statut` | integer | Status (0-3, see status table) |

### Amount Fields

| Field | Type | Description |
|-------|------|-------------|
| `total_ht` | float | Total excluding tax |
| `total_tva` | float | Total VAT amount |
| `total_ttc` | float | Total including tax |
| `totalpaid` | float | Total amount paid (calculated) |
| `totalcreditnotes` | float | Total credit notes used (calculated) |
| `totaldeposits` | float | Total deposits used (calculated) |
| `remaintopay` | float | Remaining amount to pay (calculated) |

### Payment Fields

| Field | Type | Description |
|-------|------|-------------|
| `cond_reglement_id` | integer | Payment term ID |
| `mode_reglement_id` | integer | Payment mode ID |
| `fk_account` | integer | Bank account ID |

### Other Fields

| Field | Type | Description |
|-------|------|-------------|
| `note_private` | string | Private note (internal) |
| `note_public` | string | Public note (visible to customer) |
| `lines` | array | Invoice lines (items) |
| `contacts_ids` | array | Associated contacts |
| `linked_objects` | object | Linked objects (orders, etc.) |
| `array_options` | object | Custom/extra fields |

### Invoice Types

| Value | Constant | Description |
|-------|----------|-------------|
| 0 | TYPE_STANDARD | Standard invoice |
| 1 | TYPE_REPLACEMENT | Replacement invoice |
| 2 | TYPE_CREDIT_NOTE | Credit note |
| 3 | TYPE_DEPOSIT | Deposit invoice |
| 4 | TYPE_SITUATION | Situation invoice |

### Invoice Status

| Value | Description |
|-------|-------------|
| 0 | Draft |
| 1 | Validated (Unpaid) |
| 2 | Paid |
| 3 | Cancelled |

---

## Invoice Line Object

### Main Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Line ID |
| `fk_facture` | integer | Parent invoice ID |
| `fk_product` | integer | Product/Service ID |
| `product_type` | integer | 0=Product, 1=Service, 9=Special |
| `description` | string | Line description |
| `label` | string | Short label |
| `qty` | float | Quantity |
| `subprice` | float | Unit price excluding tax |
| `remise_percent` | float | Discount percentage |
| `tva_tx` | float | VAT rate |
| `localtax1_tx` | float | Local tax 1 rate |
| `localtax2_tx` | float | Local tax 2 rate |
| `total_ht` | float | Total excluding tax |
| `total_tva` | float | Total VAT |
| `total_ttc` | float | Total including tax |
| `rang` | integer | Line position/order |
| `date_start` | timestamp | Start date (for services) |
| `date_end` | timestamp | End date (for services) |
| `fk_parent_line` | integer | Parent line ID (for sub-items) |
| `fk_unit` | integer | Unit ID |
| `special_code` | integer | Special code |
| `situation_percent` | float | Situation percentage |
| `ref_ext` | string | External reference |

---

## Notes

### Access Control
- External users can only access invoices linked to their third party (company)
- Internal users can only see invoices of customers they manage, unless they have "See all" permission
- The `id` field cannot be modified when updating invoices

### Payment Calculations
- `totalpaid`, `totalcreditnotes`, `totaldeposits`, and `remaintopay` are calculated automatically when retrieving invoices
- These calculated fields provide real-time payment status

### Invoice Validation
- Invoices must be validated before they can receive payments
- Draft invoices can be modified freely
- Validated invoices have restrictions on modifications

### Multicurrency Support
- The API supports multicurrency invoices
- Use `multicurrency_amount` in payment distributions for invoices in foreign currencies
- Amounts can be specified in either default currency or invoice currency, but not both

### Contact Types
Available contact types for invoices:
- `BILLING` - Billing contact
- `SHIPPING` - Shipping contact
- `CUSTOMER` - Customer contact

### Security
- Description and label fields are sanitized using `restricthtml` to prevent XSS attacks
- File paths and sensitive data are cleaned from responses
- API key authentication required for all endpoints
