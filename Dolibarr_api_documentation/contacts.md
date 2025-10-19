# Contacts API

The Contacts API allows you to manage contacts (people/addresses) in your Dolibarr instance. You can create, read, update, delete contacts, manage their categories, and create user accounts from contacts.

## Endpoints

- [Get a contact](#get-a-contact)
- [Get contact by email](#get-contact-by-email)
- [List contacts](#list-contacts)
- [Create a contact](#create-a-contact)
- [Update a contact](#update-a-contact)
- [Delete a contact](#delete-a-contact)
- [Create user from contact](#create-user-from-contact)
- [Get contact categories](#get-contact-categories)
- [Add category to contact](#add-category-to-contact)
- [Remove category from contact](#remove-category-from-contact)

---

## Get a contact

Retrieve detailed information about a specific contact.

```
GET /contacts/{id}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of contact (use 0 for specimen/template) |
| `includecount` | integer | query | No | 0 | Count and return number of elements the contact is used as a link for |
| `includeroles` | integer | query | No | 0 | Include roles of the contact |

### Permissions Required

- `societe->contact->lire` (read contact permission)

### Response

Returns a contact object with the following fields:

```json
{
  "id": 1,
  "lastname": "Dupont",
  "firstname": "Jean",
  "civility_code": "MR",
  "poste": "Sales Manager",
  "address": "123 Main Street",
  "zip": "75001",
  "town": "Paris",
  "state_code": "75",
  "state_id": 75,
  "country_id": 1,
  "country_code": "FR",
  "email": "jean.dupont@example.com",
  "phone": "+33 1 23 45 67 89",
  "phone_mobile": "+33 6 12 34 56 78",
  "phone_perso": "+33 1 98 76 54 32",
  "fax": "+33 1 23 45 67 90",
  "socid": 5,
  "fk_soc": 5,
  "statut": 1,
  "priv": 0,
  "birthday": 567993600,
  "default_lang": "fr_FR",
  "no_email": 0,
  "ref_ext": "EXT-001",
  "socialnetworks": {
    "linkedin": "jean-dupont",
    "twitter": "@jeandupont"
  },
  "note_public": "Public notes",
  "note_private": "Private notes",
  "date_creation": 1704067200,
  "date_modification": 1706745600,
  "user_creation": 1,
  "user_modification": 1
}
```

### Example Requests

**Basic request:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With reference counts:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts/1?includecount=1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With roles:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts/1?includeroles=1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Get specimen/template:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts/0' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or access not allowed |
| 404 | Contact not found |

---

## Get contact by email

Retrieve contact information by email address.

```
GET /contacts/email/{email}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `email` | string | path | Yes | - | Email address of the contact |
| `includecount` | integer | query | No | 0 | Count and return number of elements the contact is used as a link for |
| `includeroles` | integer | query | No | 0 | Include roles of the contact |

### Permissions Required

- `societe->contact->lire` (read contact permission)

### Response

Returns a contact object (same structure as GET /contacts/{id})

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts/email/jean.dupont@example.com' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or access not allowed |
| 404 | Contact not found |

---

## List contacts

Retrieve a list of contacts with optional filtering and pagination.

```
GET /contacts
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `sortfield` | string | query | No | `t.rowid` | Field to sort by |
| `sortorder` | string | query | No | `ASC` | Sort order (`ASC` or `DESC`) |
| `limit` | integer | query | No | 100 | Maximum number of contacts to return |
| `page` | integer | query | No | 0 | Page number (0-indexed) |
| `thirdparty_ids` | string | query | No | - | Filter by third party IDs (comma-separated, e.g., '1,2,3') |
| `category` | integer | query | No | 0 | Filter by category ID |
| `sqlfilters` | string | query | No | - | Additional SQL filters |
| `includecount` | integer | query | No | 0 | Count and return number of elements the contact is used as a link for |
| `includeroles` | integer | query | No | 0 | Include roles of the contact |

### SQL Filters Syntax

Use the `sqlfilters` parameter to apply custom filters:

```
(t.lastname:like:'Dupont%') and (t.email:!=:'')
```

Operators: `like`, `=`, `<`, `>`, `<=`, `>=`, `!=`, `is:NULL`

### Permissions Required

- `societe->contact->lire` (read contact permission)

### Response

Returns an array of contact objects:

```json
[
  {
    "id": 1,
    "lastname": "Dupont",
    "firstname": "Jean",
    "email": "jean.dupont@example.com",
    "phone": "+33 1 23 45 67 89",
    "socid": 5,
    "statut": 1
  },
  {
    "id": 2,
    "lastname": "Martin",
    "firstname": "Marie",
    "email": "marie.martin@example.com",
    "phone": "+33 1 98 76 54 32",
    "socid": 8,
    "statut": 1
  }
]
```

### Example Requests

**Basic list:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With pagination:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts?limit=50&page=0' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter by third party:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts?thirdparty_ids=5,8' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter by category:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts?category=3' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With SQL filters:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts?sqlfilters=(t.lastname:like:%27Dupont%25%27)' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Sort by lastname descending:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts?sortfield=t.lastname&sortorder=DESC' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | No contacts found |
| 503 | Error when retrieving contact list or invalid SQL filters |

---

## Create a contact

Create a new contact.

```
POST /contacts
```

### Permissions Required

- `societe->contact->creer` (create contact permission)

### Request Body

Required fields are marked with *

```json
{
  "lastname": "Dubois",           // * Last name (required)
  "firstname": "Sophie",           // First name
  "civility_code": "MME",         // Civility code (MR, MME, MLE, etc.)
  "poste": "Marketing Director",   // Position/Job title
  "address": "456 Avenue des Champs",
  "zip": "75008",
  "town": "Paris",
  "state_id": 75,                 // Department ID
  "country_id": 1,                // Country ID
  "email": "sophie.dubois@example.com",
  "phone": "+33 1 11 22 33 44",
  "phone_mobile": "+33 6 55 66 77 88",
  "phone_perso": "+33 1 99 88 77 66",
  "fax": "+33 1 11 22 33 45",
  "socid": 10,                    // Third party ID (company)
  "priv": 0,                      // 0=Public, 1=Private
  "statut": 1,                    // 0=Inactive, 1=Active
  "birthday": 631152000,          // Unix timestamp
  "default_lang": "fr_FR",
  "no_email": 0,                  // 0=Can receive emails, 1=Unsubscribed
  "ref_ext": "EXT-002",
  "note_public": "Public notes about contact",
  "note_private": "Private notes about contact"
}
```

### Response

Returns the ID of the created contact:

```json
3
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/contacts' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "lastname": "Dubois",
    "firstname": "Sophie",
    "email": "sophie.dubois@example.com",
    "phone": "+33 1 11 22 33 44",
    "socid": 10,
    "poste": "Marketing Director"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Missing required field (lastname) |
| 401 | Insufficient rights |
| 500 | Error creating contact |

---

## Update a contact

Update an existing contact's information.

```
PUT /contacts/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the contact to update |

### Permissions Required

- `societe->contact->creer` (create/modify contact permission)

### Request Body

Send only the fields you want to update:

```json
{
  "firstname": "Sophie-Marie",
  "poste": "Chief Marketing Officer",
  "phone_mobile": "+33 6 99 88 77 66",
  "email": "sophie.dubois-new@example.com"
}
```

### Response

Returns the updated contact object (same structure as GET /contacts/{id})

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/contacts/1' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "poste": "Senior Sales Manager",
    "phone_mobile": "+33 6 11 22 33 44"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Contact not found |
| 500 | Error updating contact (returns false) |

---

## Delete a contact

Delete a contact from the system.

```
DELETE /contacts/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the contact to delete |

### Permissions Required

- `societe->contact->supprimer` (delete contact permission)

### Response

Returns result code:

```json
1
```

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/contacts/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Contact not found |
| 500 | Error when deleting contact |

---

## Create user from contact

Create an external user account from an existing contact.

```
POST /contacts/{id}/createUser
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the contact |

### Permissions Required

- `societe->contact->lire` (read contact permission)
- `user->user->creer` (create user permission)

### Request Body

Required fields are marked with *

```json
{
  "login": "sdubois",        // * Login username (required)
  "password": "SecurePass123" // * User password (required)
}
```

### Response

Returns the ID of the created user:

```json
42
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/contacts/3/createUser' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "login": "sdubois",
    "password": "SecurePass123"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Missing required field (login or password) |
| 401 | User doesn't have permission |
| 404 | Contact not found |
| 500 | User not created |

---

## Get contact categories

Retrieve all categories associated with a contact.

```
GET /contacts/{id}/categories
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the contact |
| `sortfield` | string | query | No | `s.rowid` | Field to sort by |
| `sortorder` | string | query | No | `ASC` | Sort order (`ASC` or `DESC`) |
| `limit` | integer | query | No | 0 | Maximum number of categories to return (0=all) |
| `page` | integer | query | No | 0 | Page number (0-indexed) |

### Permissions Required

- `categorie->lire` (read category permission)

### Response

Returns an array of category objects:

```json
[
  {
    "id": 5,
    "label": "VIP Clients",
    "description": "High priority contacts",
    "color": "#ff0000",
    "type": 4
  },
  {
    "id": 8,
    "label": "Newsletter Subscribers",
    "description": "Contacts subscribed to newsletter",
    "color": "#00ff00",
    "type": 4
  }
]
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/contacts/1/categories' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | No category found |
| 503 | Error when retrieving category list |

---

## Add category to contact

Associate a category with a contact.

```
POST /contacts/{id}/categories/{category_id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the contact |
| `category_id` | integer | path | Yes | ID of the category to add |

### Permissions Required

- `societe->contact->creer` (create/modify contact permission)

### Response

Returns the updated contact object

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/contacts/1/categories/5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | Insufficient rights or access not allowed |
| 404 | Contact or category not found |

---

## Remove category from contact

Remove the association between a category and a contact.

```
DELETE /contacts/{id}/categories/{category_id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the contact |
| `category_id` | integer | path | Yes | ID of the category to remove |

### Permissions Required

- `societe->contact->creer` (create/modify contact permission)

### Response

Returns the updated contact object

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/contacts/1/categories/5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | Insufficient rights or access not allowed |
| 404 | Contact or category not found |

---

## Contact Object

### Main Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Contact ID (rowid) |
| `lastname` | string | Last name (required) |
| `firstname` | string | First name |
| `civility_code` | string | Civility code (MR, MME, MLE, etc.) |
| `civility_id` | string | Civility code (alias) |
| `poste` | string | Position/Job title |
| `email` | string | Email address |
| `phone` | string | Professional phone |
| `phone_mobile` | string | Mobile phone |
| `phone_perso` | string | Personal phone |
| `fax` | string | Fax number |
| `socid` / `fk_soc` | integer | Third party (company) ID |
| `statut` | integer | 0=Inactive, 1=Active |
| `priv` | integer | Contact visibility (0=Public, 1=Private) |

### Address Fields

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | Street address |
| `zip` | string | Postal/ZIP code |
| `town` | string | City/Town |
| `state_id` | integer | State/Department ID |
| `state_code` | string | State/Department code |
| `state` | string | State/Department name |
| `country_id` | integer | Country ID |
| `country_code` | string | Country code (ISO 3166-1 alpha-2) |
| `country` | string | Country name |

### Additional Fields

| Field | Type | Description |
|-------|------|-------------|
| `ref_ext` | string | External reference |
| `birthday` | integer | Birthday (Unix timestamp) |
| `default_lang` | string | Default language code |
| `no_email` | integer | Email opt-out (0=Can receive, 1=Unsubscribed) |
| `photo` | string | Photo filename |
| `socialnetworks` | object | Social network usernames |
| `note_public` | string | Public notes |
| `note_private` | string | Private notes |
| `canvas` | string | Canvas type |

### Status/Prospect Fields

| Field | Type | Description |
|-------|------|-------------|
| `fk_stcommcontact` | integer | Contact prospect status |
| `fk_prospectlevel` | string | Prospect level |

### System Fields

| Field | Type | Description |
|-------|------|-------------|
| `entity` | integer | Multi-company entity ID |
| `date_creation` / `datec` | integer | Creation date (Unix timestamp) |
| `date_modification` / `tms` | integer | Last modification date (Unix timestamp) |
| `user_creation` / `fk_user_creat` | integer | User who created the contact |
| `user_modification` / `fk_user_modif` | integer | User who last modified the contact |
| `import_key` | string | Import key for bulk operations |

### Reference Count Fields (when includecount=1)

| Field | Type | Description |
|-------|------|-------------|
| `ref_facturation` | integer | Number of invoices linked |
| `ref_contrat` | integer | Number of contracts linked |
| `ref_commande` | integer | Number of orders linked |
| `ref_propal` | integer | Number of proposals linked |

### Civility Codes

Common values for `civility_code`:

| Code | Description |
|------|-------------|
| `MR` | Mister |
| `MME` | Madam |
| `MLE` | Miss |
| `DR` | Doctor |
| `PROF` | Professor |

### Status Values

| Value | Description |
|-------|-------------|
| 0 | Inactive |
| 1 | Active |

### Privacy Values (priv)

| Value | Description |
|-------|-------------|
| 0 | Public contact (visible to all) |
| 1 | Private contact (restricted visibility) |

---

## Notes

- The `lastname` field is mandatory when creating a contact
- External users can only access contacts linked to their third party (company)
- Internal users can only see contacts of customers they manage, unless they have the "See all" permission
- The `id` field cannot be modified when updating a contact
- Some fields are automatically cleaned from the response for security reasons
- When searching by email, the email parameter is case-sensitive
- The `socialnetworks` field stores JSON data with social network usernames
- Dates are returned as Unix timestamps (seconds since January 1, 1970)
- The API automatically handles both `socid` and `fk_soc` fields (they are aliases)
- Contact categories use type 4 in the Dolibarr categories system
