# Products API

The Products API allows you to manage products and services in your Dolibarr instance. You can create, read, update, delete products, manage categories, pricing, purchase prices, product variants, attributes, subproducts, and stock information.

## Endpoints

### Product Management
- [Get a product by ID](#get-a-product-by-id)
- [Get a product by ref](#get-a-product-by-ref)
- [Get a product by ref_ext](#get-a-product-by-ref_ext)
- [Get a product by barcode](#get-a-product-by-barcode)
- [List products](#list-products)
- [Create a product](#create-a-product)
- [Update a product](#update-a-product)
- [Delete a product](#delete-a-product)

### Subproducts/Kits
- [Get subproducts](#get-subproducts)
- [Add subproduct](#add-subproduct)
- [Remove subproduct](#remove-subproduct)

### Categories
- [Get product categories](#get-product-categories)

### Pricing
- [Get prices per segment](#get-prices-per-segment)
- [Get prices per customer](#get-prices-per-customer)
- [Get prices per quantity](#get-prices-per-quantity)

### Purchase Prices
- [Get purchase prices for a product](#get-purchase-prices-for-a-product)
- [List all purchase prices](#list-all-purchase-prices)
- [Add/Update purchase price](#addupdate-purchase-price)
- [Delete purchase price](#delete-purchase-price)

### Product Attributes
- [Get attributes](#get-attributes)
- [Get attribute by ID](#get-attribute-by-id)
- [Get attribute by ref](#get-attribute-by-ref)
- [Get attribute by ref_ext](#get-attribute-by-ref_ext)
- [Create attribute](#create-attribute)
- [Update attribute](#update-attribute)
- [Delete attribute](#delete-attribute)

### Attribute Values
- [Get attribute values](#get-attribute-values)
- [Get attribute values by ref](#get-attribute-values-by-ref)
- [Get attribute value by ID](#get-attribute-value-by-id)
- [Get attribute value by ref](#get-attribute-value-by-ref)
- [Add attribute value](#add-attribute-value)
- [Update attribute value](#update-attribute-value)
- [Delete attribute value by ID](#delete-attribute-value-by-id)
- [Delete attribute value by ref](#delete-attribute-value-by-ref)

### Product Variants
- [Get product variants](#get-product-variants)
- [Get product variants by ref](#get-product-variants-by-ref)
- [Add variant](#add-variant)
- [Add variant by product ref](#add-variant-by-product-ref)
- [Update variant](#update-variant)
- [Delete variant](#delete-variant)

### Stock
- [Get product stock](#get-product-stock)

---

## Get a product by ID

Retrieve detailed information about a specific product by its ID.

```
GET /products/{id}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of product |
| `includestockdata` | integer | query | No | 0 | Load stock information (slower) |
| `includesubproducts` | boolean | query | No | false | Load information about subproducts |
| `includeparentid` | boolean | query | No | false | Load ID of parent product (if variant) |
| `includetrans` | boolean | query | No | false | Load translations of label and description |

### Permissions Required

- `produit->lire` (read product permission)

### Response

Returns a product object. See [Product Object Fields](./products/api_fields_product.md) for complete field reference.

```json
{
  "id": 1,
  "ref": "PROD001",
  "label": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with USB receiver",
  "type": 0,
  "status": 1,
  "status_buy": 1,
  "price": 29.99,
  "price_ttc": 35.99,
  "price_min": 25.00,
  "tva_tx": "20.000",
  "barcode": "1234567890123",
  "weight": 0.15,
  "weight_units": 0,
  "length": 10,
  "width": 6,
  "height": 4,
  "surface": 60,
  "volume": 240,
  "stock_reel": 150,
  "stock_theorique": 150
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/1?includestockdata=1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Bad value for parameter id |
| 401 | Access not allowed for login |
| 403 | User doesn't have permission |
| 404 | Product not found |

---

## Get a product by ref

Retrieve product information using the product reference.

```
GET /products/ref/{ref}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `ref` | string | path | Yes | - | Product reference |
| `includestockdata` | integer | query | No | 0 | Load stock information |
| `includesubproducts` | boolean | query | No | false | Load information about subproducts |
| `includeparentid` | boolean | query | No | false | Load ID of parent product |
| `includetrans` | boolean | query | No | false | Load translations |

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/ref/PROD001' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Get a product by ref_ext

Retrieve product information using the external reference.

```
GET /products/ref_ext/{ref_ext}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `ref_ext` | string | path | Yes | - | External reference |
| `includestockdata` | integer | query | No | 0 | Load stock information |
| `includesubproducts` | boolean | query | No | false | Load information about subproducts |
| `includeparentid` | boolean | query | No | false | Load ID of parent product |
| `includetrans` | boolean | query | No | false | Load translations |

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/ref_ext/EXT-001' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Get a product by barcode

Retrieve product information using the barcode.

```
GET /products/barcode/{barcode}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `barcode` | string | path | Yes | - | Product barcode |
| `includestockdata` | integer | query | No | 0 | Load stock information |
| `includesubproducts` | boolean | query | No | false | Load information about subproducts |
| `includeparentid` | boolean | query | No | false | Load ID of parent product |
| `includetrans` | boolean | query | No | false | Load translations |

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/barcode/1234567890123' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## List products

Retrieve a list of products with optional filtering and pagination.

```
GET /products
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `sortfield` | string | query | No | `t.ref` | Field to sort by |
| `sortorder` | string | query | No | `ASC` | Sort order (`ASC` or `DESC`) |
| `limit` | integer | query | No | 100 | Maximum number of products to return |
| `page` | integer | query | No | 0 | Page number (0-indexed) |
| `mode` | integer | query | No | 0 | 0=all, 1=only products, 2=only services |
| `category` | integer | query | No | 0 | Filter by category ID |
| `sqlfilters` | string | query | No | - | Additional SQL filters |
| `ids_only` | boolean | query | No | false | Return only product IDs (faster) |
| `variant_filter` | integer | query | No | 0 | 0=all, 1=no variants, 2=parent of variants, 3=variants only |
| `pagination_data` | boolean | query | No | false | Include pagination metadata |
| `includestockdata` | integer | query | No | 0 | Load stock information |

### SQL Filters Syntax

Use the `sqlfilters` parameter to apply custom filters:

```
(t.tobuy:=:0) and (t.tosell:=:1)
```

Operators: `like`, `=`, `<`, `>`, `<=`, `>=`, `!=`

### Permissions Required

- `produit->lire` (read product permission)

### Response

Returns an array of product objects:

```json
[
  {
    "id": 1,
    "ref": "PROD001",
    "label": "Wireless Mouse",
    "type": 0,
    "status": 1
  },
  {
    "id": 2,
    "ref": "PROD002",
    "label": "Keyboard",
    "type": 0,
    "status": 1
  }
]
```

### Response with Pagination Data

When `pagination_data=true`:

```json
{
  "data": [
    {
      "id": 1,
      "ref": "PROD001",
      "label": "Wireless Mouse"
    }
  ],
  "pagination": {
    "total": 150,
    "page": 0,
    "page_count": 2,
    "limit": 100
  }
}
```

### Example Requests

**Basic list:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter only products (not services):**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products?mode=1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Get IDs only for faster response:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products?ids_only=true' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With pagination data:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products?pagination_data=true&limit=50' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter by category:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products?category=5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With SQL filters:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products?sqlfilters=(t.tosell:=:1)' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 403 | User doesn't have permission |
| 404 | No product found |
| 503 | Error when retrieving product list or invalid SQL filters |

---

## Create a product

Create a new product or service.

```
POST /products
```

### Permissions Required

- `produit->creer` (create product permission)

### Request Body

Required fields are marked with *

```json
{
  "ref": "PROD003",              // * Product reference (unique)
  "label": "New Product",        // * Product label/name
  "description": "Product description",
  "type": 0,                     // 0=Product, 1=Service
  "status": 1,                   // 0=Off, 1=On sale
  "status_buy": 1,               // 0=Off, 1=Can purchase
  "price": 49.99,
  "price_base_type": "HT",       // HT or TTC
  "tva_tx": 20.0,
  "barcode": "1234567890124",
  "weight": 0.5,
  "length": 20,
  "width": 10,
  "height": 5,
  "customcode": "CUSTOM001",
  "country_id": 1,
  "duration": "1y"               // For services: duration
}
```

### Response

Returns the ID of the created product:

```json
3
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/products' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "ref": "PROD003",
    "label": "Premium Headphones",
    "description": "Noise-cancelling wireless headphones",
    "type": 0,
    "status": 1,
    "status_buy": 1,
    "price": 149.99,
    "tva_tx": 20.0,
    "barcode": "9876543210123"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Missing required field (ref or label) |
| 401 | Insufficient rights |
| 500 | Error creating product |

---

## Update a product

Update an existing product. Price will be updated only if option is set on "One price per product".

```
PUT /products/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the product to update |

### Permissions Required

- `produit->creer` (create/modify product permission)

### Request Body

Send only the fields you want to update:

```json
{
  "label": "Updated Product Name",
  "description": "Updated description",
  "price": 59.99,
  "status": 1
}
```

**Important Notes:**
- The `id` field cannot be modified
- The `stock_reel` field cannot be updated here - use the `/stockmovements` endpoint instead
- Price updates only work if `PRODUCT_PRICE_UNIQ` configuration is enabled

### Response

Returns the updated product object.

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/products/1' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "label": "Wireless Mouse Pro",
    "price": 34.99,
    "description": "Professional ergonomic wireless mouse"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Attempt to update stock_reel field |
| 401 | User doesn't have permission |
| 404 | Product not found |
| 500 | Error updating product |

---

## Delete a product

Delete a product from the system.

```
DELETE /products/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the product to delete |

### Permissions Required

- `produit->supprimer` (delete product permission)

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
  'https://your-dolibarr.com/api/index.php/products/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Product not found |
| 409 | Can't delete, product is probably in use |
| 500 | Can't delete, error occurs |

---

## Get subproducts

Get the list of subproducts for a product (for kits/virtual products).

```
GET /products/{id}/subproducts
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of parent product |

### Permissions Required

- `produit->lire` (read product permission)

### Response

```json
[
  {
    "rowid": 5,
    "qty": 2,
    "fk_product_type": 0,
    "label": "Component A",
    "incdec": 1,
    "ref": "COMP-A",
    "fk_association": 10,
    "rang": 1
  },
  {
    "rowid": 6,
    "qty": 1,
    "fk_product_type": 0,
    "label": "Component B",
    "incdec": 1,
    "ref": "COMP-B",
    "fk_association": 11,
    "rang": 2
  }
]
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/1/subproducts' \
  -H 'DOLAPIKEY: your_api_key_here'
```

---

## Add subproduct

Link a product/service to a parent product/service (create kit).

```
POST /products/{id}/subproducts/add
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of parent product |
| `subproduct_id` | integer | body | Yes | - | ID of child product |
| `qty` | integer | body | Yes | - | Quantity of child product |
| `incdec` | integer | body | No | 1 | 1=Increase/decrease stock of child with parent |

### Permissions Required

- `produit->creer` (create product permission)

### Request Body

```json
{
  "subproduct_id": 5,
  "qty": 2,
  "incdec": 1
}
```

### Response

Returns the result code.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/products/1/subproducts/add' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "subproduct_id": 5,
    "qty": 2,
    "incdec": 1
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 500 | Error adding product child |

---

## Remove subproduct

Unlink a product/service from a parent product/service.

```
DELETE /products/{id}/subproducts/remove/{subproduct_id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of parent product |
| `subproduct_id` | integer | path | Yes | ID of child product to remove |

### Permissions Required

- `produit->creer` (create product permission)

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/products/1/subproducts/remove/5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 500 | Error while removing product child |

---

## Get product categories

Get all categories assigned to a product.

```
GET /products/{id}/categories
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of product |
| `sortfield` | string | query | No | `s.rowid` | Sort field |
| `sortorder` | string | query | No | `ASC` | Sort order |
| `limit` | integer | query | No | 0 | Limit for list |
| `page` | integer | query | No | 0 | Page number |

### Permissions Required

- `categorie->lire` (read category permission)

### Response

Returns an array of category objects.

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/1/categories' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | No category found |
| 503 | Error when retrieving category list |

---

## Get prices per segment

Get prices per customer segment for a product (requires multi-price mode enabled).

```
GET /products/{id}/selling_multiprices/per_segment
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of product |

### Permissions Required

- `produit->lire` (read product permission)
- Requires `PRODUIT_MULTIPRICES` configuration enabled

### Response

```json
{
  "multiprices": [0, 29.99, 34.99, 39.99],
  "multiprices_inc_tax": [0, 35.99, 41.99, 47.99],
  "multiprices_min": [0, 25.00, 30.00, 35.00],
  "multiprices_min_inc_tax": [0, 30.00, 36.00, 42.00],
  "multiprices_vat": [0, "20.000", "20.000", "20.000"],
  "multiprices_base_type": ["HT", "HT", "HT", "HT"]
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/1/selling_multiprices/per_segment' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | API not available: multi-price mode not enabled |
| 401 | User doesn't have permission |
| 404 | Product not found |
| 503 | Error when retrieving prices list |

---

## Get prices per customer

Get customer-specific prices for a product (requires customer price mode enabled).

```
GET /products/{id}/selling_multiprices/per_customer
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of product |
| `thirdparty_id` | string | query | No | Filter by third party ID |

### Permissions Required

- `produit->lire` (read product permission)
- Requires `PRODUIT_CUSTOMER_PRICES` configuration enabled

### Response

Returns an array of customer-specific price objects.

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/1/selling_multiprices/per_customer?thirdparty_id=5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | API not available: customer price mode not enabled |
| 401 | User doesn't have permission or accessing unauthorized customer |
| 404 | Product or prices not found |

---

## Get prices per quantity

Get quantity-based prices for a product (requires quantity pricing enabled).

```
GET /products/{id}/selling_multiprices/per_quantity
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of product |

### Permissions Required

- `produit->lire` (read product permission)
- Requires `PRODUIT_CUSTOMER_PRICES_BY_QTY` configuration enabled

### Response

```json
{
  "prices_by_qty": 1,
  "prices_by_qty_list": [
    {
      "rowid": 1,
      "quantity": 10,
      "price": 27.99,
      "unitprice": 27.99,
      "remise_percent": 5
    },
    {
      "rowid": 2,
      "quantity": 50,
      "price": 24.99,
      "unitprice": 24.99,
      "remise_percent": 10
    }
  ]
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/1/selling_multiprices/per_quantity' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | API not available: quantity pricing not enabled |
| 401 | User doesn't have permission |
| 404 | Product not found |
| 503 | Error when retrieving prices list |

---

## Get purchase prices for a product

Get all purchase prices for a specific product.

```
GET /products/{id}/purchase_prices
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | No | ID of product |
| `ref` | string | query | No | Ref of product |
| `ref_ext` | string | query | No | External ref of product |
| `barcode` | string | query | No | Barcode of product |

**Note:** At least one parameter (id, ref, ref_ext, or barcode) must be provided.

### Permissions Required

- `produit->lire` (read product permission)

### Response

Returns an array of purchase price objects with supplier information.

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/1/purchase_prices' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Bad value for parameters |
| 401 | User doesn't have permission |
| 403 | Forbidden |
| 404 | Product not found |

---

## List all purchase prices

Get a list of all purchase prices for products with optional filtering.

```
GET /products/purchase_prices
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `sortfield` | string | query | No | `t.ref` | Sort field |
| `sortorder` | string | query | No | `ASC` | Sort order |
| `limit` | integer | query | No | 100 | Maximum number to return |
| `page` | integer | query | No | 0 | Page number |
| `mode` | integer | query | No | 0 | 0=all, 1=only products, 2=only services |
| `category` | integer | query | No | 0 | Filter by category ID |
| `supplier` | integer | query | No | 0 | Filter by supplier ID |
| `sqlfilters` | string | query | No | - | Additional SQL filters |

### Permissions Required

- `produit->lire` (read product permission)

### Response

Returns an array indexed by product ID containing purchase price arrays.

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/purchase_prices?supplier=5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or external user accessing other suppliers |
| 404 | No product found |
| 503 | Error when retrieving product list or invalid SQL filters |

---

## Add/Update purchase price

Add or update purchase price for a product with a supplier.

```
POST /products/{id}/purchase_prices
```

### Parameters

All parameters except `id` are sent in the request body.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | ID of product (path) |
| `qty` | float | Yes | Minimum quantity |
| `buyprice` | float | Yes | Purchase price for quantity |
| `price_base_type` | string | Yes | `HT` or `TTC` |
| `fourn_id` | integer | Yes | Supplier ID |
| `availability` | integer | Yes | Product availability |
| `ref_fourn` | string | Yes | Supplier reference |
| `tva_tx` | float | Yes | VAT rate (e.g., 8.5) |
| `charges` | float | No | Additional costs |
| `remise_percent` | float | No | Discount percentage |
| `remise` | float | No | Discount amount |
| `newnpr` | integer | No | Set NPR or not |
| `delivery_time_days` | integer | No | Delivery time in days |
| `supplier_reputation` | string | No | `FAVORITE`, `DONOTORDER`, or empty |
| `localtaxes_array` | array | No | Local taxes info |
| `newdefaultvatcode` | string | No | Default VAT code |
| `multicurrency_buyprice` | float | No | Price in currency |
| `multicurrency_price_base_type` | string | No | `HT` or `TTC` in currency |
| `multicurrency_tx` | float | No | Currency rate |
| `multicurrency_code` | string | No | Currency code |
| `desc_fourn` | string | No | Custom description |
| `barcode` | string | No | Barcode |
| `fk_barcode_type` | integer | No | Barcode type |

### Permissions Required

- `produit->creer` (create product permission)

### Request Body

```json
{
  "qty": 1,
  "buyprice": 15.50,
  "price_base_type": "HT",
  "fourn_id": 3,
  "availability": 3,
  "ref_fourn": "SUP-PROD-001",
  "tva_tx": 20.0,
  "delivery_time_days": 5,
  "supplier_reputation": "FAVORITE"
}
```

### Response

Returns the ID of the purchase price record.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/products/1/purchase_prices' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "qty": 1,
    "buyprice": 15.50,
    "price_base_type": "HT",
    "fourn_id": 3,
    "availability": 3,
    "ref_fourn": "SUP-PROD-001",
    "tva_tx": 20.0
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or external user adding for other supplier |
| 404 | Product or supplier not found |
| 500 | Error adding supplier or updating buy price |

---

## Delete purchase price

Delete a purchase price record for a product.

```
DELETE /products/{id}/purchase_prices/{priceid}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | Product ID |
| `priceid` | integer | path | Yes | Purchase price ID |

### Permissions Required

- `produit->supprimer` (delete product permission)

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/products/1/purchase_prices/5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Product not found |

---

## Get attributes

Get a list of product attributes.

```
GET /products/attributes
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `sortfield` | string | query | No | `t.ref` | Sort field |
| `sortorder` | string | query | No | `ASC` | Sort order |
| `limit` | integer | query | No | 100 | Maximum number to return |
| `page` | integer | query | No | 0 | Page number |
| `sqlfilters` | string | query | No | - | SQL filters (e.g., `(t.ref:like:color)`) |

### Permissions Required

- `produit->lire` (read product permission)

### Response

```json
[
  {
    "id": 1,
    "ref": "COLOR",
    "ref_ext": "",
    "label": "Color",
    "position": 1,
    "entity": 1
  },
  {
    "id": 2,
    "ref": "SIZE",
    "ref_ext": "",
    "label": "Size",
    "position": 2,
    "entity": 1
  }
]
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/attributes' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | No product attribute found |
| 503 | Error when retrieving product attribute list or invalid SQL filters |

---

## Get attribute by ID

Get a specific product attribute by its ID.

```
GET /products/attributes/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of attribute |

### Permissions Required

- `produit->lire` (read product permission)

### Response

```json
{
  "id": 1,
  "ref": "COLOR",
  "ref_ext": "",
  "label": "Color",
  "position": 1,
  "entity": 1,
  "is_used_by_products": 15
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/attributes/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Product attribute not found |

---

## Get attribute by ref

Get a product attribute by its reference.

```
GET /products/attributes/ref/{ref}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `ref` | string | path | Yes | Reference of attribute |

### Permissions Required

- `produit->lire` (read product permission)

### Response

```json
{
  "id": 1,
  "ref": "COLOR",
  "ref_ext": "",
  "label": "Color",
  "rang": 1,
  "position": 1,
  "entity": 1,
  "is_used_by_products": 15
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/attributes/ref/COLOR' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Attribute not found |

---

## Get attribute by ref_ext

Get a product attribute by its external reference.

```
GET /products/attributes/ref_ext/{ref_ext}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `ref_ext` | string | path | Yes | External reference of attribute |

### Permissions Required

- `produit->lire` (read product permission)

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/attributes/ref_ext/EXT-COLOR' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Attribute not found |
| 500 | System error |

---

## Create attribute

Create a new product attribute.

```
POST /products/attributes
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ref` | string | Yes | Reference of attribute |
| `label` | string | Yes | Label of attribute |
| `ref_ext` | string | No | External reference |

### Permissions Required

- `produit->creer` (create product permission)

### Request Body

```json
{
  "ref": "MATERIAL",
  "label": "Material",
  "ref_ext": "EXT-MAT"
}
```

### Response

Returns the ID of the created attribute.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/products/attributes' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "ref": "MATERIAL",
    "label": "Material"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 500 | Error creating new attribute |

---

## Update attribute

Update an existing product attribute.

```
PUT /products/attributes/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of attribute |

### Permissions Required

- `produit->creer` (create product permission)

### Request Body

Send only the fields you want to update:

```json
{
  "label": "Updated Label",
  "ref_ext": "NEW-EXT-REF"
}
```

### Response

Returns the updated attribute object.

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/products/attributes/1' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "label": "Product Color"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Attribute not found |
| 500 | Error fetching or updating attribute |

---

## Delete attribute

Delete a product attribute.

```
DELETE /products/attributes/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of attribute |

### Permissions Required

- `produit->supprimer` (delete product permission)

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/products/attributes/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 500 | Error deleting attribute |

---

## Get attribute values

Get all values for a specific attribute by attribute ID.

```
GET /products/attributes/{id}/values
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of attribute |

### Permissions Required

- `produit->lire` (read product permission)

### Response

```json
[
  {
    "id": 1,
    "fk_product_attribute": 1,
    "ref": "RED",
    "value": "Red"
  },
  {
    "id": 2,
    "fk_product_attribute": 1,
    "ref": "BLUE",
    "value": "Blue"
  }
]
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/attributes/1/values' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Attribute values not found |

---

## Get attribute values by ref

Get all values for a specific attribute by attribute reference.

```
GET /products/attributes/ref/{ref}/values
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `ref` | string | path | Yes | Reference of attribute |

### Permissions Required

- `produit->lire` (read product permission)

### Response

Returns an array of attribute value objects.

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/attributes/ref/COLOR/values' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |

---

## Get attribute value by ID

Get a specific attribute value by its ID.

```
GET /products/attributes/values/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of attribute value |

### Permissions Required

- `produit->lire` (read product permission)

### Response

```json
{
  "id": 1,
  "fk_product_attribute": 1,
  "ref": "RED",
  "value": "Red"
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/attributes/values/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Attribute value not found |

---

## Get attribute value by ref

Get a specific attribute value by attribute ID and value reference.

```
GET /products/attributes/{id}/values/ref/{ref}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of attribute |
| `ref` | string | path | Yes | Reference of attribute value |

### Permissions Required

- `produit->lire` (read product permission)

### Response

```json
{
  "id": 1,
  "fk_product_attribute": 1,
  "ref": "RED",
  "value": "Red"
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/attributes/1/values/ref/RED' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Attribute value not found |

---

## Add attribute value

Add a new value to a product attribute.

```
POST /products/attributes/{id}/values
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of attribute |
| `ref` | string | body | Yes | Reference of value |
| `value` | string | body | Yes | Label/value of the attribute value |

### Permissions Required

- `produit->creer` (create product permission)

### Request Body

```json
{
  "ref": "GREEN",
  "value": "Green"
}
```

### Response

Returns the ID of the created attribute value.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/products/attributes/1/values' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "ref": "GREEN",
    "value": "Green"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or missing required fields |
| 500 | Error creating new attribute value |

---

## Update attribute value

Update an existing attribute value.

```
PUT /products/attributes/values/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of attribute value |

### Permissions Required

- `produit->creer` (create product permission)

### Request Body

Send only the fields you want to update:

```json
{
  "value": "Dark Green",
  "ref": "DGREEN"
}
```

### Response

Returns the updated attribute value object.

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/products/attributes/values/1' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "value": "Bright Red"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Attribute value not found |
| 500 | Error fetching or updating attribute |

---

## Delete attribute value by ID

Delete an attribute value by its ID.

```
DELETE /products/attributes/values/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of attribute value |

### Permissions Required

- `produit->supprimer` (delete product permission)

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/products/attributes/values/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 500 | Error deleting attribute value |

---

## Delete attribute value by ref

Delete an attribute value by attribute ID and value reference.

```
DELETE /products/attributes/{id}/values/ref/{ref}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of attribute |
| `ref` | string | path | Yes | Reference of attribute value |

### Permissions Required

- `produit->supprimer` (delete product permission)

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/products/attributes/1/values/ref/RED' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Attribute value not found |
| 500 | Error deleting attribute value |

---

## Get product variants

Get all variants for a product.

```
GET /products/{id}/variants
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of product |
| `includestock` | integer | query | No | 0 | 1=Include stock data for each variant |

### Permissions Required

- `produit->lire` (read product permission)
- `stock->lire` (if includestock=1)

### Response

```json
[
  {
    "id": 10,
    "fk_product_parent": 1,
    "fk_product_child": 15,
    "variation_price": 5.00,
    "variation_price_percentage": false,
    "variation_weight": 0,
    "attributes": [
      {
        "fk_prod_attr": 1,
        "fk_prod_attr_val": 2
      }
    ]
  }
]
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/1/variants?includestock=1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 500 | System error |

---

## Get product variants by ref

Get all variants for a product by its reference.

```
GET /products/ref/{ref}/variants
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `ref` | string | path | Yes | Reference of product |

### Permissions Required

- `produit->lire` (read product permission)

### Response

Returns an array of variant objects.

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/ref/PROD001/variants' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Product not found |
| 500 | System error |

---

## Add variant

Create a new product variant.

```
POST /products/{id}/variants
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of parent product |
| `weight_impact` | float | body | Yes | Weight impact of variant |
| `price_impact` | float | body | Yes | Price impact of variant |
| `price_impact_is_percent` | boolean | body | Yes | Is price impact a percentage |
| `features` | array | body | Yes | List of attribute pairs (id_attribute=>id_value) |
| `reference` | string | body | No | Customized reference |
| `ref_ext` | string | body | No | External reference |

### Permissions Required

- `produit->creer` (create product permission)

### Request Body

```json
{
  "weight_impact": 0.1,
  "price_impact": 5.00,
  "price_impact_is_percent": false,
  "features": {
    "1": "2",
    "3": "5"
  },
  "reference": "PROD001-RED-L"
}
```

**Note:** `features` is an object where keys are attribute IDs and values are attribute value IDs.

### Response

Returns the ID of the created variant.

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/products/1/variants' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "weight_impact": 0,
    "price_impact": 10,
    "price_impact_is_percent": false,
    "features": {
      "1": "2",
      "2": "4"
    }
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or invalid features |
| 404 | Product not found |
| 500 | Error creating new product variant |

---

## Add variant by product ref

Create a new product variant using product reference.

```
POST /products/ref/{ref}/variants
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `ref` | string | path | Yes | Reference of parent product |
| `weight_impact` | float | body | Yes | Weight impact |
| `price_impact` | float | body | Yes | Price impact |
| `price_impact_is_percent` | boolean | body | Yes | Is price impact a percentage |
| `features` | array | body | Yes | List of attribute pairs |

### Permissions Required

- `produit->creer` (create product permission)

### Request Body

```json
{
  "weight_impact": 0.1,
  "price_impact": 5.00,
  "price_impact_is_percent": false,
  "features": {
    "1": "2",
    "3": "5"
  }
}
```

### Response

Returns the ID of the created variant (or existing variant if combination already exists).

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/products/ref/PROD001/variants' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "weight_impact": 0,
    "price_impact": 0,
    "price_impact_is_percent": false,
    "features": {"1": "3"}
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Product, attribute, or attribute value not found |
| 500 | Error creating new product variant |

---

## Update variant

Update an existing product variant.

```
PUT /products/variants/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of variant |

### Permissions Required

- `produit->creer` (create product permission)

### Request Body

Send only the fields you want to update:

```json
{
  "variation_price": 7.50,
  "variation_weight": 0.2
}
```

### Response

Returns 1 on success.

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/products/variants/10' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "variation_price": 12.00
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 500 | Error editing variant |

---

## Delete variant

Delete a product variant.

```
DELETE /products/variants/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of variant |

### Permissions Required

- `produit->supprimer` (delete product permission)

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/products/variants/10' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 500 | Error deleting variant |

---

## Get product stock

Get stock data for a product, optionally filtered by warehouse.

```
GET /products/{id}/stock
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of product |
| `selected_warehouse_id` | integer | query | No | Filter by specific warehouse ID |

### Permissions Required

- `produit->lire` (read product permission)
- `stock->lire` (read stock permission)

### Response

```json
{
  "stock_warehouses": {
    "1": {
      "id": 1,
      "ref": "WH-001",
      "label": "Main Warehouse",
      "stock": 100,
      "pmp": 20.50
    },
    "2": {
      "id": 2,
      "ref": "WH-002",
      "label": "Secondary Warehouse",
      "stock": 50,
      "pmp": 20.50
    }
  }
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/1/stock' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter by warehouse:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/products/1/stock?selected_warehouse_id=1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | No stock found |
| 500 | System error |

---

## Product Object

### Product Types

| Value | Description |
|-------|-------------|
| 0 | Product (physical item) |
| 1 | Service |

### Product Status

| Field | Value | Description |
|-------|-------|-------------|
| `status` | 0 | Not on sale |
| `status` | 1 | On sale |
| `status_buy` | 0 | Not available for purchase |
| `status_buy` | 1 | Available for purchase |

### Variant Filter Values

| Value | Description |
|-------|-------------|
| 0 | All products |
| 1 | Products without variants |
| 2 | Parent products (have variants) |
| 3 | Variant products only |

---

## Notes

- External users (suppliers) can only access products and prices related to their company
- The `stock_reel` field cannot be updated via the product endpoints - use the Stock Movements API instead
- Price updates only work if the "One price per product" mode is enabled (`PRODUCT_PRICE_UNIQ`)
- Multi-price features require specific configuration flags to be enabled in Dolibarr
- Product attributes and variants are advanced features for managing product variations (e.g., size, color)
- When creating variants, the `features` parameter must contain valid attribute ID and attribute value ID pairs

---

## See Also

- [Product Fields Reference](./products/api_fields_product.md) - Complete list of product object fields
- Stock Movements API - For managing product stock levels
- Categories API - For managing product categories
