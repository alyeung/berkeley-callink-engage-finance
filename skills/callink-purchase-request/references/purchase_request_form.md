# CalLink Create Purchase Request Form Reference

Target route:
`https://callink.berkeley.edu/actionCenter/organization/<org_slug>/Finance/CreatePurchaseRequest`

---

## 1. Request Details

| Field | Required | DOM ID / Name | Notes / Options |
| :--- | :---: | :--- | :--- |
| **Subject** | Yes | `#Subject` | Clear event/expense title. Add `1 of 2` / `2 of 2` if splitting across accounts or >6 items. |
| **Description** | No | `#Description` | Brief purpose of expense and event context; include split instructions if applicable. |
| **Requested Amount** | Yes | `#RequestedAmount` | Numeric total (`type="number"`). Decimals like `470.94` are valid on submit (`form.noValidate` is `true` even though HTML `step="1"` flags `stepMismatch`). |
| **Categories** | Yes | `#CategoryId` | For student reimbursements, select `Reimbursement` (value `1352`). See full list below. |
| **Account** | Yes | `#accountSelectButton` (sets hidden `#AccountId`) | Opens Kendo modal `#selectAccountContainer` (`#AccountGrid`); click `a.account-picker[id="<account_id>"]` to populate `#AccountId`. **Never select `SUMMARY`.** |

<details>
<summary>All Categories dropdown options (`#CategoryId`)</summary>

| Value | Label |
| :--- | :--- |
| `5028` | `ASUC Credit Card Purchase (select Instant Card unless no digital pay accepted)` |
| `4391` | `ASUC Instant Card Purchase (mobile temp-use card) - preferred` |
| `12774` | `Awards` |
| `6609` | `Bank/Wire transfer - fee involved, pre-discussed with ASUC Finance (admin use only)` |
| `1357` | `Contracted Service` |
| `18492` | `Deposit` |
| `14413` | `Deposit (admin use only)` |
| `14027` | `Donation` |
| `14028` | `Grants` |
| `18480` | `Internal Transfer` |
| `1353` | `Payment to Vendor` |
| `1359` | `Purchase Order (NON-campus services) - COMPANIES ONLY` |
| `1358` | `Purchase Order-Campus Services (Event Services, Facilities, etc.)` |
| `1352` | `Reimbursement` |
| `1360` | `Stipend` |
| `1361` | `Transfer between Accounts` |
| `14066` | `UC Berkeley Journal Transfer (admin use only)` |
| `1362` | `X-Adjustment (Admin use only)` |

</details>

---

## 2. Payee Information

All address fields are required (except `Street Continued`). International mailing addresses are not supported. For businesses/orgs, put organization name in `First Name` and `ATTN: Contact Name` in `Last Name`.

| Field | DOM ID |
| :--- | :--- |
| **First Name** | `#PayeeFirstName` |
| **Last Name** | `#PayeeLastName` |
| **Street** | `#PayeeStreet` |
| **Street Continued (Optional)** | `#PayeeStreet2` |
| **City** | `#PayeeCity` |
| **State/Province** | `#PayeeState` |
| **ZIP/Postal Code** | `#PayeeZipCode` |

---

## 3. Standard Campus Questions (1–6 & Event Details)

| Question | Required | DOM ID / Options | Notes |
| :--- | :---: | :--- | :--- |
| **1. UCB Student / Faculty / Staff?** | Yes | Radio `#28262917` (`YES`) + `#answerTextBox-28262917-free` (UID)<br>Radio `#28262918` (`No`) | Enter **UID** from Campus Directory / CalCentral (**never** a 10-digit `303...` or `304...` SID, or SSN). |
| **1a. UID Certification** | Yes | Checkbox `#49448409` | Must be checked to certify UID (or non-UC affiliate status). |
| **2. Payee's Email Address** | Yes | `#answerTextBox-13557646-free` | Use campus `.edu` email for UCB affiliates; **not** the requestor's email. |
| **3. Payee's Phone Number** | Yes | `#answerTextBox-13557622-free` | Payee's phone number; **not** the requestor's phone. |
| **4. Expenditure Action** | Yes | `#dropDown-2483087` | `13557685`: Mail to Payee<br>`13557687`: Hold for Pickup at SU Finance AP/AR Window, 432A Eshleman Hall<br>`43040847`: Direct Deposit - Answer Question 6.<br>`43139369`: International Wire Transfer<br>`43139370`: Other (please answer Question 5 Special Instructions) |
| **5. Special Instructions** | Conditional | `#answerTextBox-13557872-free` | **Leave blank unless** `Requested Amount` differs from receipt total, receipt is split across accounts, or payee differs from receipt name. Put routine receipt summaries in `#Description`. |
| **6. Direct Deposit** | Conditional | `#dropDown-11669296` | Required if Q4 = `Direct Deposit`:<br>`43040801`: Payee has already successfully completed the direct deposit sign up form<br>`43040802`: Payee hasn't completed the sign up form, but will complete the form within 3 business days of today |
| **Event Details** | Recommended | `#answerTextBox-13557733-free` | Event date(s), event location(s), estimated # of attendees. |

---

## 4. Expense Items (`Item #1` – `Item #6`)

`Item #1` fields (except `Invoice Number` and `Additional Misc. Information`) are required. Upload **one consolidated PDF (`< 4 MB`) per item**. Do not use Items #2–#6 for extra pages of Item #1.

`Type of Expense` options (same labels across Items #1–#6):
- `Contracted Services/Performer`
- `Copies/Printing`
- `Food`
- `Stipend`
- `Supplies`
- `Travel`
- `Other`

### Item DOM IDs

| Field | Item #1 (Required) | Item #2 | Item #3 | Item #4 | Item #5 | Item #6 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Date of Expense** | `#answerTextBox-40496834-free` | `#answerTextBox-40496855-free` | `#answerTextBox-40496874-free` | `#answerTextBox-40496889-free` | `#answerTextBox-40496903-free` | `#answerTextBox-40496921-free` |
| **Type of Expense** | `#dropDown-10532762` | `#dropDown-10532777` | `#dropDown-10532788` | `#dropDown-10532798` | `#dropDown-10532807` | `#dropDown-10532820` |
| **Vendor Name** | `#answerTextBox-40496846-free` | `#answerTextBox-40496866-free` | `#answerTextBox-40496882-free` | `#answerTextBox-40496897-free` | `#answerTextBox-40496911-free` | `#answerTextBox-40496929-free` |
| **Location (City, State)** | `#answerTextBox-40496847-free` | `#answerTextBox-40496868-free` | `#answerTextBox-40496883-free` | `#answerTextBox-40496898-free` | `#answerTextBox-40496916-free` | `#answerTextBox-40496930-free` |
| **Invoice Number** | `#answerTextBox-40496848-free` | `#answerTextBox-40496870-free` | `#answerTextBox-40496884-free` | `#answerTextBox-40496899-free` | `#answerTextBox-40496917-free` | `#answerTextBox-40496931-free` |
| **Total of Expense** | `#answerTextBox-40496852-free` | `#answerTextBox-40496871-free` | `#answerTextBox-40496885-free` | `#answerTextBox-40496900-free` | `#answerTextBox-40496918-free` | `#answerTextBox-40496932-free` |
| **Additional Misc. Info** | `#answerTextBox-40496853-free` | `#answerTextBox-40496872-free` | `#answerTextBox-40496886-free` | `#answerTextBox-40496901-free` | `#answerTextBox-40496919-free` | `#answerTextBox-40496933-free` |
| **Upload File Button** | `#fileUploadQuestion-10532772` | `#fileUploadQuestion-10532786` | `#fileUploadQuestion-10532795` | `#fileUploadQuestion-10532805` | `#fileUploadQuestion-10532818` | `#fileUploadQuestion-10532827` |

*(Note: Upload buttons open a jQuery UI dialog fetched from `.../Finance/FileUploadQuestion/GetFileUploadDialog` containing `<input type="file" name="PostedFile">`. Once uploaded, the filename appears in `pageResponse.Files[fu...].TemporaryFileName`. Leave `Additional Misc. Information` blank unless listing a mileage rate or explaining a multi-account split. The final submit button is `#saveButton` — never click `#saveButton` automatically.)*
