---
stadium_asset: data-model
app: RMB_Onboarding
file_guid: 87ea91de-6125-4686-8437-806216cb0ec0
designer_version: 6.14.3378.13771
selected_package: 3f1ddf96-3519-47b8-905d-b44703776f78.sapz
extracted_from: C:\Stadium 6 Web Apps\87ea91de-6125-4686-8437-806216cb0ec0
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Data model — RMB_Onboarding

> Entities + fields reconciled across SQL queries/views, stored procedures and web-service calls (union by name). Every field carries a `[from …]` locator naming its exact source.

## Tier-A — entities & fields

### Administrators  ·  sources: stored-procedure  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `Administrators.AdminCapacity` : AnsiString [from stored-procedure: dbo.prc_Administrators_Insert]  _(+1 more)_
- `Administrators.AdminFullName` : AnsiString [from stored-procedure: dbo.prc_Administrators_Insert]  _(+1 more)_
- `Administrators.AdminID_Passport` : AnsiString [from stored-procedure: dbo.prc_Administrators_Insert]  _(+1 more)_
- `Administrators.AdministratorsID` : Int32 [from stored-procedure: dbo.prc_Administrators_Update]  _(+1 more)_
- `Administrators.ApplicationID` : Int32 [from stored-procedure: dbo.prc_Administrators_GetList]  _(+1 more)_
- `Administrators.IDType` : Int16 [from stored-procedure: dbo.prc_Administrators_Insert]  _(+1 more)_

### ApplicationDocument  ·  sources: stored-procedure  ·  operations: SELECT
- `ApplicationDocument.ApplicationID` : Int64 [from stored-procedure: dbo.sp_ApplicationDocument_Get]
> related shapes: `tblApplications` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ApplicationSteps  ·  sources: stored-procedure  ·  operations: SELECT
- `ApplicationSteps.ApplicationID` : Int64 [from stored-procedure: dbo.sp_Application_Steps_Get]
- `ApplicationSteps.ProductID` : Int64 [from stored-procedure: dbo.sp_Application_Steps_Get]
> related shapes: `tblApplications` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BalanceHostToHost  ·  sources: stored-procedure  ·  operations: INSERT
- `BalanceHostToHost.ApplicationID` : Int64 [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.Daily` : Boolean [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.Friday` : Boolean [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.InteremStatementType` : Int32 [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.Monday` : Boolean [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.RepeatEvery` : Int32 [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.Saturday` : Boolean [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.ScheduleName` : AnsiString [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.SortTransactionsOnDate` : Int32 [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.StatementsFileRequired` : Int32 [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.Sunday` : Boolean [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.Thursday` : Boolean [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.TimeFrom` : Time [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.TimeTo` : Time [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.Tuesday` : Boolean [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]
- `BalanceHostToHost.Wedenesday` : Boolean [from stored-procedure: dbo.sp_BalanceHostToHost_Insert]

### BalanceSetup  ·  sources: stored-procedure  ·  operations: INSERT
- `BalanceSetup.AccountGroup` : Boolean [from stored-procedure: dbo.sp_BalanceSetup_Insert]
- `BalanceSetup.AccountSubGroup` : Boolean [from stored-procedure: dbo.sp_BalanceSetup_Insert]
- `BalanceSetup.ApplicationID` : Int64 [from stored-procedure: dbo.sp_BalanceSetup_Insert]
- `BalanceSetup.ConsolidatedBalances` : Boolean [from stored-procedure: dbo.sp_BalanceSetup_Insert]
- `BalanceSetup.HostToHost` : Boolean [from stored-procedure: dbo.sp_BalanceSetup_Insert]
- `BalanceSetup.Movement` : Boolean [from stored-procedure: dbo.sp_BalanceSetup_Insert]
- `BalanceSetup.ProductsAccountBalances` : Boolean [from stored-procedure: dbo.sp_BalanceSetup_Insert]

### BalanceStatementBankAccount  ·  sources: stored-procedure  ·  operations: DELETE, INSERT, SELECT
- `BalanceStatementBankAccount.ApplicationID` : Int64 [from stored-procedure: dbo.sp_BalanceStatementBankAccount_Insert]  _(+2 more)_
- `BalanceStatementBankAccount.BankAccountID` : Int64 [from stored-procedure: dbo.sp_BalanceStatementBankAccount_Insert]
- `BalanceStatementBankAccount.ID` : Int64 [from stored-procedure: dbo.sp_BalanceStatementBankAccount_Delete]
> related shapes: `BankAccount` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankAccount  ·  sources: stored-procedure  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `BankAccount.AccountName` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]  _(+1 more)_
- `BankAccount.ApplicationID` : Int64 [from stored-procedure: dbo.sp_BankAccount_Insert]  _(+2 more)_
- `BankAccount.BankAccountID` : Int64 [from stored-procedure: dbo.sp_BankAccount_Get]  _(+2 more)_
- `BankAccount.BankAccountOwner` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]
- `BankAccount.BankAccountShortName` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]  _(+1 more)_
- `BankAccount.BankAccountStyle` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]  _(+1 more)_
- `BankAccount.BankName` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]
- `BankAccount.BankNumber` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]
- `BankAccount.BicSwiftCode` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]  _(+1 more)_
- `BankAccount.BranchName` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]  _(+1 more)_
- `BankAccount.BranchSortCode` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]  _(+1 more)_
- `BankAccount.Country` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]  _(+1 more)_
- `BankAccount.Currency` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]  _(+1 more)_
- `BankAccount.CustomerID` : Int64 [from stored-procedure: dbo.sp_BankAccount_Insert]
- `BankAccount.IBAN` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]
- `BankAccount.Serial` : AnsiString [from stored-procedure: dbo.sp_BankAccount_Insert]
> related shapes: `BalanceStatementBankAccount` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ClientApplications  ·  sources: stored-procedure  ·  operations: SELECT
- `ClientApplications.UserAllocated` : AnsiString [from stored-procedure: dbo.sp_ClientApplications_Get]
> related shapes: `ClientApplicationsAllocate`, `ClientApplicationsUnallocated`, `Clients`, `tblApplications` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ClientApplicationsAllocate  ·  sources: stored-procedure  ·  operations: INSERT
- `ClientApplicationsAllocate.ApplicationID` : Int64 [from stored-procedure: dbo.sp_ClientApplications_Allocate_Insert]
- `ClientApplicationsAllocate.UserEmail` : AnsiString [from stored-procedure: dbo.sp_ClientApplications_Allocate_Insert]
- `ClientApplicationsAllocate.UserGuid` : AnsiString [from stored-procedure: dbo.sp_ClientApplications_Allocate_Insert]
- `ClientApplicationsAllocate.UserName` : AnsiString [from stored-procedure: dbo.sp_ClientApplications_Allocate_Insert]
> related shapes: `ClientApplications`, `Clients`, `tblApplications` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ClientApplicationsUnallocated  ·  sources: stored-procedure  ·  operations: SELECT
- `ClientApplicationsUnallocated.UserAllocated` : AnsiString [from stored-procedure: dbo.sp_ClientApplicationsUnallocated_Get]
> related shapes: `ClientApplications`, `Clients`, `tblApplications` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### Clients  ·  sources: web-service  ·  operations: SELECT
- _(fields not modelled for this endpoint)_
> related shapes: `ClientApplications`, `ClientApplicationsAllocate`, `ClientApplicationsUnallocated`, `ClientsAndProducts`, `tbl_ClientDetails` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ClientsAndProducts  ·  sources: web-service  ·  operations: SELECT
- _(fields not modelled for this endpoint)_
> related shapes: `Clients` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### Collections  ·  sources: stored-procedure  ·  operations: INSERT, UPDATE
- `Collections.ApplicationID` : Int32 [from stored-procedure: dbo.prc_Collections_Insert]  _(+1 more)_
- `Collections.CollAppAccountNumber` : AnsiString [from stored-procedure: dbo.prc_Collections_Insert]  _(+1 more)_
- `Collections.CollAppBranchCode` : AnsiString [from stored-procedure: dbo.prc_Collections_Insert]  _(+1 more)_
- `Collections.CollAppClientName` : AnsiString [from stored-procedure: dbo.prc_Collections_Insert]  _(+1 more)_
> related shapes: `tbl_CollectionsApplication`, `tbl_CollectionsContactPerson` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### FileImage  ·  sources: stored-procedure  ·  operations: SELECT
- `FileImage.ApplicationID` : Int64 [from stored-procedure: dbo.sp_FileImage_Get]
- `FileImage.Count` : Int32 [from stored-procedure: dbo.sp_FileImage_Get]

### History  ·  sources: stored-procedure  ·  operations: SELECT
- `History.ApplicationID` : Int64 [from stored-procedure: dbo.sp_History_Get]
> related shapes: `WOHistory` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ModularEntity  ·  sources: stored-procedure  ·  operations: INSERT, SELECT, UPDATE
- `ModularEntity.ApplicationID` : Int32 [from stored-procedure: dbo.prc_ModularEntity_Insert]  _(+1 more)_
- `ModularEntity.ModEntityID` : Int32 [from stored-procedure: dbo.prc_ModularEntity_Update]
- `ModularEntity.ModEntityName` : AnsiString [from stored-procedure: dbo.prc_ModularEntity_Insert]  _(+1 more)_
- `ModularEntity.ModEntityNumber` : AnsiString [from stored-procedure: dbo.prc_ModularEntity_Insert]  _(+1 more)_

### ModularInformation  ·  sources: stored-procedure  ·  operations: INSERT, UPDATE
- `ModularInformation._ApplicationID` : Int32 [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularAandBSignatories` : Boolean [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularCashman` : Boolean [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularCashmanReports` : Boolean [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularCollections` : Boolean [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularFTPDeliveryMechanism` : Boolean [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularLinkCCNNumber1` : AnsiString [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularLinkCCNNumber2` : AnsiString [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularLinkCCNNumber3` : AnsiString [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularLinkCCNNumber4` : AnsiString [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularLinkCCNNumber5` : AnsiString [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularLinkCCNNumber6` : AnsiString [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularNAEDO` : Boolean [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularNominatedAccountPayments` : Int32 [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularOnceOffPayments` : Boolean [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularOnlineSettlementLimits` : Boolean [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_
- `ModularInformation.ModularTransfers` : Boolean [from stored-procedure: dbo.prc_ModularInformation_Insert]  _(+1 more)_

### PartiesHeirarchy  ·  sources: stored-procedure  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `PartiesHeirarchy.ApplicationID` : Int32 [from stored-procedure: dbo.prc_PartiesHeirarchy_GetList]  _(+1 more)_
- `PartiesHeirarchy.HeirarchyEntitiesID` : AnsiString [from stored-procedure: dbo.prc_PartiesHeirarchy_Insert]  _(+1 more)_
- `PartiesHeirarchy.PartiesHAccountName` : AnsiString [from stored-procedure: dbo.prc_PartiesHeirarchy_Insert]  _(+1 more)_
- `PartiesHeirarchy.PartiesHAccountNumber` : AnsiString [from stored-procedure: dbo.prc_PartiesHeirarchy_Insert]  _(+1 more)_
- `PartiesHeirarchy.PartiesHeirarchyID` : Int32 [from stored-procedure: dbo.prc_PartiesHeirarchy_Disable]  _(+1 more)_
> related shapes: `PartiesHeirarchyHeirarchyEntitiesID`, `tbl_PartiesHeirarchyTable` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### PartiesHeirarchyHeirarchyEntitiesID  ·  sources: stored-procedure  ·  operations: UPDATE
- `PartiesHeirarchyHeirarchyEntitiesID.HeirarchyEntitiesID` : Int32 [from stored-procedure: dbo.prc_PartiesHeirarchy_HeirarchyEntitiesID_Update]
- `PartiesHeirarchyHeirarchyEntitiesID.PartiesHeirarchyID` : Int32 [from stored-procedure: dbo.prc_PartiesHeirarchy_HeirarchyEntitiesID_Update]
> related shapes: `PartiesHeirarchy` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ProductAdminSetup  ·  sources: stored-procedure  ·  operations: INSERT
- `ProductAdminSetup.ApplicationID` : Int64 [from stored-procedure: dbo.sp_Product_AdminSetup_Insert]
- `ProductAdminSetup.Instant` : Boolean [from stored-procedure: dbo.sp_Product_AdminSetup_Insert]
- `ProductAdminSetup.Mobile` : Boolean [from stored-procedure: dbo.sp_Product_AdminSetup_Insert]
- `ProductAdminSetup.Normal` : Boolean [from stored-procedure: dbo.sp_Product_AdminSetup_Insert]
- `ProductAdminSetup.SynchronisedPayment` : Boolean [from stored-procedure: dbo.sp_Product_AdminSetup_Insert]
- `ProductAdminSetup.Urgent` : Boolean [from stored-procedure: dbo.sp_Product_AdminSetup_Insert]
- `ProductAdminSetup.ValueDated` : Boolean [from stored-procedure: dbo.sp_Product_AdminSetup_Insert]

### ProductPaymentsAndFeatures  ·  sources: stored-procedure  ·  operations: INSERT
- `ProductPaymentsAndFeatures.AdhocBOPThirdParty` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.ApplicationID` : Int64 [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.AvailableFundsCheck` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.BillsSARSDOL` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.CreditFacility` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.EarlyClearingValidation` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.ManageOrders` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.MyBills` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.PayAlert` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.PostingConsolidated` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.PostingItemised` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.PostingType` : Int32 [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.RecurringPayments` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.ReRelease` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.ThirdPartyPayment` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.ViewAvailableBalance` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.ViewBeneficiaryDetail` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]
- `ProductPaymentsAndFeatures.ViewLimits` : Boolean [from stored-procedure: dbo.sp_Product_PaymentsAndFeatures_Insert]

### ProductServiceSetup  ·  sources: stored-procedure  ·  operations: INSERT
- `ProductServiceSetup.ApplicationID` : Int64 [from stored-procedure: dbo.sp_Product_ServiceSetup_Insert]
- `ProductServiceSetup.AuthoriseOwnBeneficiary` : Boolean [from stored-procedure: dbo.sp_Product_ServiceSetup_Insert]
- `ProductServiceSetup.Beneficiary` : Boolean [from stored-procedure: dbo.sp_Product_ServiceSetup_Insert]
- `ProductServiceSetup.Biller` : Boolean [from stored-procedure: dbo.sp_Product_ServiceSetup_Insert]
- `ProductServiceSetup.BOPThirdParty` : Boolean [from stored-procedure: dbo.sp_Product_ServiceSetup_Insert]
- `ProductServiceSetup.PayAlert` : Boolean [from stored-procedure: dbo.sp_Product_ServiceSetup_Insert]
- `ProductServiceSetup.PaymentType` : Boolean [from stored-procedure: dbo.sp_Product_ServiceSetup_Insert]

### SignatoriesUserDisabled  ·  sources: stored-procedure  ·  operations: DELETE
- `SignatoriesUserDisabled.ApplicationID` : Int64 [from stored-procedure: dbo.sp_Signatories_UserDisabled_Disable]
- `SignatoriesUserDisabled.UserID` : Int64 [from stored-procedure: dbo.sp_Signatories_UserDisabled_Disable]
> related shapes: `User` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### Signatory  ·  sources: stored-procedure  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `Signatory.ApplicationID` : Int64 [from stored-procedure: dbo.sp_Signatory_Create]  _(+2 more)_
- `Signatory.DriversLicenceNumber` : AnsiString [from stored-procedure: dbo.sp_Signatory_Create]
- `Signatory.IdentificationNumber` : AnsiString [from stored-procedure: dbo.sp_Signatory_Create]
- `Signatory.IdentificationType` : Int16 [from stored-procedure: dbo.sp_Signatory_Create]
- `Signatory.IDType` : Int16 [from stored-procedure: dbo.prc_Signatories_Update]
- `Signatory.PassportNumber` : AnsiString [from stored-procedure: dbo.sp_Signatory_Create]
- `Signatory.SignatoryID` : Int64 [from stored-procedure: dbo.sp_Signatories_Disable]
- `Signatory.SignatureDesignation` : AnsiString [from stored-procedure: dbo.prc_Signatories_Update]
- `Signatory.SignatureFieldID` : Int32 [from stored-procedure: dbo.prc_Signatories_Update]
- `Signatory.SignatureFullNameSurname` : AnsiString [from stored-procedure: dbo.prc_Signatories_Update]
- `Signatory.SignatureIDPassport` : AnsiString [from stored-procedure: dbo.prc_Signatories_Update]
- `Signatory.SignatureInitials` : AnsiString [from stored-procedure: dbo.prc_Signatories_Update]
- `Signatory.UserID` : Int64 [from stored-procedure: dbo.sp_Signatory_Create]
- `Signatory.UserMiddleName` : AnsiString [from stored-procedure: dbo.sp_Signatory_Create]
- `Signatory.UserName` : AnsiString [from stored-procedure: dbo.sp_Signatory_Create]
- `Signatory.UserSurname` : AnsiString [from stored-procedure: dbo.sp_Signatory_Create]
> related shapes: `SignatoryAddress`, `SignatorySigningArrangements` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### SignatoryAddress  ·  sources: stored-procedure  ·  operations: INSERT
- `SignatoryAddress.City` : AnsiString [from stored-procedure: dbo.sp_SignatoryAddress_Insert]
- `SignatoryAddress.CountryId` : Int16 [from stored-procedure: dbo.sp_SignatoryAddress_Insert]
- `SignatoryAddress.PhysicalAddress` : AnsiString [from stored-procedure: dbo.sp_SignatoryAddress_Insert]
- `SignatoryAddress.PostalCode` : AnsiString [from stored-procedure: dbo.sp_SignatoryAddress_Insert]
- `SignatoryAddress.Province` : AnsiString [from stored-procedure: dbo.sp_SignatoryAddress_Insert]
- `SignatoryAddress.ProvinceID` : Int16 [from stored-procedure: dbo.sp_SignatoryAddress_Insert]
- `SignatoryAddress.SignatoryID` : Int64 [from stored-procedure: dbo.sp_SignatoryAddress_Insert]
- `SignatoryAddress.Suburb` : AnsiString [from stored-procedure: dbo.sp_SignatoryAddress_Insert]
> related shapes: `Signatory` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### SignatorySigningArrangements  ·  sources: stored-procedure  ·  operations: INSERT, SELECT
- `SignatorySigningArrangements.ApplicationID` : Int64 [from stored-procedure: dbo.sp_Signatory_SigningArrangements_Insert]  _(+1 more)_
- `SignatorySigningArrangements.Joint` : Boolean [from stored-procedure: dbo.sp_Signatory_SigningArrangements_Insert]
- `SignatorySigningArrangements.Severally` : Boolean [from stored-procedure: dbo.sp_Signatory_SigningArrangements_Insert]
- `SignatorySigningArrangements.SignatoryCount` : Int16 [from stored-procedure: dbo.sp_Signatory_SigningArrangements_Insert]
> related shapes: `Signatory` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### tbl_ApplicationForRMB  ·  sources: sql  ·  operations: —
- _(fields not modelled for this endpoint)_
> related shapes: `tblApplications` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### tbl_AppointmentOfAdmins  ·  sources: sql  ·  operations: SELECT
- `tbl_AppointmentOfAdmins._AdminID` : Int32 [from connector: get_Administrator]
- `tbl_AppointmentOfAdmins._ApplicationID` : Int64 [from connector: get_Administrator]
- `tbl_AppointmentOfAdmins.AdminCapacity` : String [from connector: get_Administrator]
- `tbl_AppointmentOfAdmins.AdminFullName` : String [from connector: get_Administrator]
- `tbl_AppointmentOfAdmins.AdminID_Passport` : String [from connector: get_Administrator]
- `tbl_AppointmentOfAdmins.IDType` : Int16 [from connector: get_Administrator]

### tbl_ClientDetails  ·  sources: sql, stored-procedure  ·  operations: INSERT, SELECT
- `tbl_ClientDetails.ClientID` : AnsiString [from stored-procedure: dbo.prc_ClientDetails_Insert]
- `tbl_ClientDetails.ClientName` : AnsiString [from connector: get_ClientDetails]  _(+1 more)_
- `tbl_ClientDetails.ClientRegistrationNumber` : AnsiString [from connector: get_ClientDetails]  _(+1 more)_
- `tbl_ClientDetails.ClientSegment` : AnsiString [from stored-procedure: dbo.prc_ClientDetails_Insert]
- `tbl_ClientDetails.ClientSurname` : AnsiString [from stored-procedure: dbo.prc_ClientDetails_Insert]
> related shapes: `Clients` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### tbl_CollectionsApplication  ·  sources: sql  ·  operations: SELECT
- `tbl_CollectionsApplication._ApplicationID` : Int64 [from connector: get_Collections]
- `tbl_CollectionsApplication._CollectionsApplicationID` : Int32 [from connector: get_Collections]
- `tbl_CollectionsApplication.CollAppAccountNumber` : String [from connector: get_Collections]
- `tbl_CollectionsApplication.CollAppBranchCode` : String [from connector: get_Collections]
- `tbl_CollectionsApplication.CollAppClientName` : String [from connector: get_Collections]
> related shapes: `Collections`, `tblApplications` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### tbl_CollectionsContactPerson  ·  sources: sql, stored-procedure  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `tbl_CollectionsContactPerson._CollectionsApplicationID` : Int32 [from connector: get_CollectionsContactPerson]
- `tbl_CollectionsContactPerson.ApplicationID` : Int32 [from stored-procedure: dbo.prc_CollectionsContactPerson_Insert]  _(+1 more)_
- `tbl_CollectionsContactPerson.ContactPersonID` : Int32 [from stored-procedure: dbo.prc_CollectionsContactPerson_Update]  _(+2 more)_
- `tbl_CollectionsContactPerson.ContPAbbreviatedName` : AnsiString [from stored-procedure: dbo.prc_CollectionsContactPerson_Insert]  _(+2 more)_
- `tbl_CollectionsContactPerson.ContPAccountNumber` : AnsiString [from stored-procedure: dbo.prc_CollectionsContactPerson_Insert]  _(+2 more)_
- `tbl_CollectionsContactPerson.ContPCompanyName` : AnsiString [from stored-procedure: dbo.prc_CollectionsContactPerson_Insert]  _(+2 more)_
- `tbl_CollectionsContactPerson.ContPContactEmail` : AnsiString [from stored-procedure: dbo.prc_CollectionsContactPerson_Insert]  _(+2 more)_
- `tbl_CollectionsContactPerson.ContPContactName` : AnsiString [from stored-procedure: dbo.prc_CollectionsContactPerson_Insert]  _(+2 more)_
- `tbl_CollectionsContactPerson.ContPContactTelNo` : AnsiString [from stored-procedure: dbo.prc_CollectionsContactPerson_Insert]  _(+2 more)_
> related shapes: `Collections` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### tbl_HeirarchyEntities  ·  sources: sql, stored-procedure  ·  operations: INSERT, SELECT, UPDATE
- `tbl_HeirarchyEntities._ApplicationID` : Int32 [from connector: get_HeirarchyEntities]  _(+2 more)_
- `tbl_HeirarchyEntities._HeirarchyEntitiesID` : Int32 [from connector: get_HeirarchyEntities]
- `tbl_HeirarchyEntities.EntityName` : AnsiString [from connector: get_HeirarchyEntities]  _(+2 more)_
- `tbl_HeirarchyEntities.EntityNumber` : AnsiString [from connector: get_HeirarchyEntities]  _(+2 more)_

### tbl_ModularForm  ·  sources: sql  ·  operations: SELECT
- _(fields not modelled for this endpoint)_
> related shapes: `tbl_ModularFormEntityTable` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### tbl_ModularFormEntityTable  ·  sources: sql  ·  operations: SELECT
- `tbl_ModularFormEntityTable._ModEntityID` : Int32 [from connector: get_ModularEntities]  _(+1 more)_
- `tbl_ModularFormEntityTable._ModularID` : Int32 [from connector: get_ModularEntities]  _(+1 more)_
- `tbl_ModularFormEntityTable.ModEntityName` : String [from connector: get_ModularEntities]  _(+1 more)_
- `tbl_ModularFormEntityTable.ModEntityNumber` : String [from connector: get_ModularEntities]  _(+1 more)_
> related shapes: `tbl_ModularForm` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### tbl_PartiesHeirarchyTable  ·  sources: sql  ·  operations: SELECT
- _(fields not modelled for this endpoint)_
> related shapes: `PartiesHeirarchy` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### tbl_SignatureField  ·  sources: sql, stored-procedure  ·  operations: DELETE, INSERT, SELECT
- `tbl_SignatureField.ApplicationID` : Int32 [from stored-procedure: dbo.prc_SignatureField_GetList]  _(+1 more)_
- `tbl_SignatureField.IDType` : Int16 [from stored-procedure: dbo.prc_SignatureField_Insert]
- `tbl_SignatureField.SignatureDesignation` : AnsiString [from stored-procedure: dbo.prc_SignatureField_Insert]
- `tbl_SignatureField.SignatureFieldID` : Int32 [from stored-procedure: dbo.prc_SignatureField_Disable]
- `tbl_SignatureField.SignatureFullNameSurname` : AnsiString [from stored-procedure: dbo.prc_SignatureField_Insert]
- `tbl_SignatureField.SignatureIDPassport` : AnsiString [from stored-procedure: dbo.prc_SignatureField_Insert]
- `tbl_SignatureField.SignatureInitials` : AnsiString [from stored-procedure: dbo.prc_SignatureField_Insert]

### tblApplications  ·  sources: sql, stored-procedure  ·  operations: INSERT, SELECT, UPDATE
- `tblApplications.ApplicationID` : Int64 [from stored-procedure: dbo.sp_Application_Create]
- `tblApplications.ClientID` : Int32 [from stored-procedure: dbo.prc_Application_Insert]
- `tblApplications.CurrentStepID` : Int64 [from stored-procedure: dbo.sp_Application_Create]
- `tblApplications.CustomerID` : Int64 [from stored-procedure: dbo.sp_Application_Create]
- `tblApplications.ProductID` : Int64 [from stored-procedure: dbo.sp_Application_Create]
- `tblApplications.UserCreatedID` : AnsiString [from stored-procedure: dbo.sp_Application_Create]  _(+1 more)_
- `tblApplications.UserCreatedName` : AnsiString [from stored-procedure: dbo.sp_Application_Create]  _(+1 more)_
- `tblApplications.WOID` : Int32 [from stored-procedure: dbo.sp_Application_Create]  _(+2 more)_
> related shapes: `ApplicationDocument`, `ApplicationSteps`, `ClientApplications`, `ClientApplicationsAllocate`, `ClientApplicationsUnallocated`, `UserApplicationSetup`, `tbl_ApplicationForRMB`, `tbl_CollectionsApplication` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### tblCfgTypeItems  ·  sources: sql  ·  operations: SELECT
- `tblCfgTypeItems.CfgTypeID` : Int64 [from connector: sqlTypeItems_Get]
- `tblCfgTypeItems.Description` : String [from connector: sqlTypeItems_Get]
- `tblCfgTypeItems.ID` : Int64 [from connector: sqlTypeItems_Get]
- `tblCfgTypeItems.Name` : String [from connector: sqlTypeItems_Get]
- `tblCfgTypeItems.TypeID` : Int32 [from connector: sqlTypeItems_Get]

### tblCountryCode_ISO3166  ·  sources: sql  ·  operations: SELECT
- `tblCountryCode_ISO3166.Country` : Int16 [from connector: sql_ProductCountries_Get]
- `tblCountryCode_ISO3166.CountryID` : Int32 [from connector: sql_ProductCountries_Get]
- `tblCountryCode_ISO3166.ID` : Int64 [from connector: sql_ProductCountries_Get]
- `tblCountryCode_ISO3166.ProductID` : String [from connector: sql_ProductCountries_Get]

### tblCurrencyCode_ISO4217  ·  sources: sql  ·  operations: SELECT
- `tblCurrencyCode_ISO4217.CurrencyCode` : String [from connector: sql_ProductCurrencies_Get]
- `tblCurrencyCode_ISO4217.CurrencyID` : Int64 [from connector: sql_ProductCurrencies_Get]
- `tblCurrencyCode_ISO4217.CurrencyName` : String [from connector: sql_ProductCurrencies_Get]
- `tblCurrencyCode_ISO4217.ID` : Int64 [from connector: sql_ProductCurrencies_Get]
- `tblCurrencyCode_ISO4217.ProductID` : Int64 [from connector: sql_ProductCurrencies_Get]

### tblCustomerDetails  ·  sources: sql, stored-procedure  ·  operations: UPDATE
- `tblCustomerDetails.CompanyRegistrationNumber` : AnsiString [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.CompanyTaxNumber` : AnsiString [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.CompanyVatNumber` : AnsiString [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.ContactPersonName` : AnsiString [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.ContactPersonSurame` : AnsiString [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.CustomerBaseCurrency` : AnsiString [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.CustomerID` : Int64 [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.Email` : AnsiString [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.FaxNumber` : AnsiString [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.PasswordExpiryFrequency` : Int16 [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.PreferredLanguage` : AnsiString [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.TelephoneNumber` : AnsiString [from stored-procedure: dbo.sp_CustomerDetails_Update]
- `tblCustomerDetails.VATIndicator` : Boolean [from stored-procedure: dbo.sp_CustomerDetails_Update]

### User  ·  sources: stored-procedure  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `User.ApplicationID` : Int64 [from stored-procedure: dbo.sp_User_Create]  _(+3 more)_
- `User.DateOfBirth` : Date [from stored-procedure: dbo.sp_User_Update]
- `User.Gender` : Int16 [from stored-procedure: dbo.sp_User_Create]  _(+1 more)_
- `User.IdentificationNumber` : AnsiString [from stored-procedure: dbo.sp_User_Create]  _(+1 more)_
- `User.IdentificationType` : Int16 [from stored-procedure: dbo.sp_User_Create]  _(+1 more)_
- `User.Language` : Int32 [from stored-procedure: dbo.sp_User_Create]  _(+1 more)_
- `User.ReceiveCommunications` : Boolean [from stored-procedure: dbo.sp_User_Create]  _(+1 more)_
- `User.ReceiveEmail` : Boolean [from stored-procedure: dbo.sp_User_Create]  _(+1 more)_
- `User.ReceiveSMS` : Boolean [from stored-procedure: dbo.sp_User_Create]  _(+1 more)_
- `User.UserID` : Int64 [from stored-procedure: dbo.sp_User_Update]  _(+2 more)_
- `User.UserMiddleName` : AnsiString [from stored-procedure: dbo.sp_User_Create]
- `User.UserName` : AnsiString [from stored-procedure: dbo.sp_User_Create]
- `User.UserSurname` : AnsiString [from stored-procedure: dbo.sp_User_Create]
> related shapes: `SignatoriesUserDisabled`, `UserAddress`, `UserApplicationSetup`, `UserContact`, `UserDetails` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserAddress  ·  sources: stored-procedure  ·  operations: INSERT
- `UserAddress.City` : AnsiString [from stored-procedure: dbo.sp_UserAddress_Insert]
- `UserAddress.CountryId` : Int16 [from stored-procedure: dbo.sp_UserAddress_Insert]
- `UserAddress.PhysicalAddress` : AnsiString [from stored-procedure: dbo.sp_UserAddress_Insert]
- `UserAddress.PostalCode` : AnsiString [from stored-procedure: dbo.sp_UserAddress_Insert]
- `UserAddress.Province` : AnsiString [from stored-procedure: dbo.sp_UserAddress_Insert]
- `UserAddress.ProvinceID` : Int16 [from stored-procedure: dbo.sp_UserAddress_Insert]
- `UserAddress.Suburb` : AnsiString [from stored-procedure: dbo.sp_UserAddress_Insert]
- `UserAddress.UserID` : Int64 [from stored-procedure: dbo.sp_UserAddress_Insert]
> related shapes: `User` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserApplicationSetup  ·  sources: stored-procedure  ·  operations: INSERT
- `UserApplicationSetup.DesignatedPerson` : Boolean [from stored-procedure: dbo.sp_UserApplicationSetup_Insert]
- `UserApplicationSetup.EmailNotificationsOnAuthorisation` : Boolean [from stored-procedure: dbo.sp_UserApplicationSetup_Insert]
- `UserApplicationSetup.EndDate` : Date [from stored-procedure: dbo.sp_UserApplicationSetup_Insert]
- `UserApplicationSetup.ResetOwnPassword` : Boolean [from stored-procedure: dbo.sp_UserApplicationSetup_Insert]
- `UserApplicationSetup.SelfServiceAdministrator` : Boolean [from stored-procedure: dbo.sp_UserApplicationSetup_Insert]
- `UserApplicationSetup.SignatoryType` : Int16 [from stored-procedure: dbo.sp_UserApplicationSetup_Insert]
- `UserApplicationSetup.StartDate` : Date [from stored-procedure: dbo.sp_UserApplicationSetup_Insert]
- `UserApplicationSetup.StartEndDateAvailable` : Boolean [from stored-procedure: dbo.sp_UserApplicationSetup_Insert]
- `UserApplicationSetup.UserID` : Int64 [from stored-procedure: dbo.sp_UserApplicationSetup_Insert]
> related shapes: `User`, `tblApplications` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserContact  ·  sources: stored-procedure  ·  operations: INSERT
- `UserContact.AlternativeTelephoneNumber` : AnsiString [from stored-procedure: dbo.sp_UserContact_Insert]
- `UserContact.EmailAddress` : AnsiString [from stored-procedure: dbo.sp_UserContact_Insert]
- `UserContact.FaxNumber` : AnsiString [from stored-procedure: dbo.sp_UserContact_Insert]
- `UserContact.MobileNumber` : AnsiString [from stored-procedure: dbo.sp_UserContact_Insert]
- `UserContact.TelephoneNumber` : AnsiString [from stored-procedure: dbo.sp_UserContact_Insert]
- `UserContact.UserID` : Int64 [from stored-procedure: dbo.sp_UserContact_Insert]
> related shapes: `User` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserDetails  ·  sources: stored-procedure  ·  operations: SELECT
- `UserDetails.ApplicationID` : Int64 [from stored-procedure: dbo.sp_UserDetails_GetList]
> related shapes: `User` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### WO  ·  sources: sql, stored-procedure  ·  operations: INSERT, UPDATE
- `WO.NextActionDate_5` : AnsiString [from stored-procedure: dbo.prc_WO_Insert]  _(+1 more)_
- `WO.NextActionDate_7` : AnsiString [from stored-procedure: dbo.prc_WO_update]
- `WO.NextActionDate_7_Flag` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.NextActionSequence_4` : Int32 [from stored-procedure: dbo.prc_WO_Insert]  _(+1 more)_
- `WO.NextActionSequence_6` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.NextActionSequence_6_DefaultFlag` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.NextActionSequence_6_Flag` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.WOID` : Int32 [from stored-procedure: dbo.prc_WO_Insert_ReturnWOID]
- `WO.WOID_1` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.WOPriorityID_3` : Int32 [from stored-procedure: dbo.prc_WO_Insert]  _(+1 more)_
- `WO.WOPriorityID_5` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.WOPriorityID_5_Flag` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.WOSource_6` : Int32 [from stored-procedure: dbo.prc_WO_Insert]  _(+1 more)_
- `WO.WOSource_8` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.WOSource_8_Flag` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.WOStatusID_2` : Int32 [from stored-procedure: dbo.prc_WO_Insert]  _(+1 more)_
- `WO.WOStatusID_4` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.WOStatusID_4_Flag` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.WOTypeID_1` : Int32 [from stored-procedure: dbo.prc_WO_Insert]  _(+1 more)_
- `WO.WOTypeID_3` : Int32 [from stored-procedure: dbo.prc_WO_update]
- `WO.WOTypeID_3_Flag` : Int32 [from stored-procedure: dbo.prc_WO_update]

### WODFileLog  ·  sources: sql  ·  operations: SELECT
- `WODFileLog._ApplicationID` : Int64 [from connector: get_ApplicationFile]
- `WODFileLog.CFFileSettingID` : Int32 [from connector: sql_GetApplicationFile]  _(+1 more)_
- `WODFileLog.FileLocation` : String [from connector: sql_GetApplicationFile]  _(+1 more)_
- `WODFileLog.FileName` : String [from connector: sql_GetApplicationFile]  _(+1 more)_
- `WODFileLog.ID` : Int64 [from connector: sql_GetApplicationFile]
- `WODFileLog.WOID` : Int32 [from connector: sql_GetApplicationFile]  _(+1 more)_

### WOHistory  ·  sources: stored-procedure  ·  operations: INSERT
- `WOHistory.WOActionDate_4` : AnsiString [from stored-procedure: dbo.prc_WOHistory_insert]
- `WOHistory.WOActionID_2` : Int32 [from stored-procedure: dbo.prc_WOHistory_insert]
- `WOHistory.WOActionNote_3` : AnsiString [from stored-procedure: dbo.prc_WOHistory_insert]
- `WOHistory.WOActionUser_5` : AnsiString [from stored-procedure: dbo.prc_WOHistory_insert]
- `WOHistory.WOID_1` : Int32 [from stored-procedure: dbo.prc_WOHistory_insert]
> related shapes: `History` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

> The design model defines 369 internal data-type instances (control/result/parameter bindings); field types above are sourced from them where concrete. Full detail is in the forensic model.json.

## Tier-A — CRUD matrix

| Entity | SELECT | INSERT | UPDATE | DELETE | Evidence |
|---|:---:|:---:|:---:|:---:|---|
| Administrators | ✓ | ✓ | ✓ | ✓ | stored-procedure |
| ApplicationDocument | ✓ |  |  |  | stored-procedure |
| ApplicationSteps | ✓ |  |  |  | stored-procedure |
| BalanceHostToHost |  | ✓ |  |  | stored-procedure |
| BalanceSetup |  | ✓ |  |  | stored-procedure |
| BalanceStatementBankAccount | ✓ | ✓ |  | ✓ | stored-procedure |
| BankAccount | ✓ | ✓ | ✓ | ✓ | stored-procedure |
| ClientApplications | ✓ |  |  |  | stored-procedure |
| ClientApplicationsAllocate |  | ✓ |  |  | stored-procedure |
| ClientApplicationsUnallocated | ✓ |  |  |  | stored-procedure |
| Clients | ✓ |  |  |  | web-service |
| ClientsAndProducts | ✓ |  |  |  | web-service |
| Collections |  | ✓ | ✓ |  | stored-procedure |
| FileImage | ✓ |  |  |  | stored-procedure |
| History | ✓ |  |  |  | stored-procedure |
| ModularEntity | ✓ | ✓ | ✓ |  | stored-procedure |
| ModularInformation |  | ✓ | ✓ |  | stored-procedure |
| PartiesHeirarchy | ✓ | ✓ | ✓ | ✓ | stored-procedure |
| PartiesHeirarchyHeirarchyEntitiesID |  |  | ✓ |  | stored-procedure |
| ProductAdminSetup |  | ✓ |  |  | stored-procedure |
| ProductPaymentsAndFeatures |  | ✓ |  |  | stored-procedure |
| ProductServiceSetup |  | ✓ |  |  | stored-procedure |
| SignatoriesUserDisabled |  |  |  | ✓ | stored-procedure |
| Signatory | ✓ | ✓ | ✓ | ✓ | stored-procedure |
| SignatoryAddress |  | ✓ |  |  | stored-procedure |
| SignatorySigningArrangements | ✓ | ✓ |  |  | stored-procedure |
| tbl_ApplicationForRMB |  |  |  |  | sql |
| tbl_AppointmentOfAdmins | ✓ |  |  |  | sql |
| tbl_ClientDetails | ✓ | ✓ |  |  | sql, stored-procedure |
| tbl_CollectionsApplication | ✓ |  |  |  | sql |
| tbl_CollectionsContactPerson | ✓ | ✓ | ✓ | ✓ | sql, stored-procedure |
| tbl_HeirarchyEntities | ✓ | ✓ | ✓ |  | sql, stored-procedure |
| tbl_ModularForm | ✓ |  |  |  | sql |
| tbl_ModularFormEntityTable | ✓ |  |  |  | sql |
| tbl_PartiesHeirarchyTable | ✓ |  |  |  | sql |
| tbl_SignatureField | ✓ | ✓ |  | ✓ | sql, stored-procedure |
| tblApplications | ✓ | ✓ | ✓ |  | sql, stored-procedure |
| tblCfgTypeItems | ✓ |  |  |  | sql |
| tblCountryCode_ISO3166 | ✓ |  |  |  | sql |
| tblCurrencyCode_ISO4217 | ✓ |  |  |  | sql |
| tblCustomerDetails |  |  | ✓ |  | sql, stored-procedure |
| User | ✓ | ✓ | ✓ | ✓ | stored-procedure |
| UserAddress |  | ✓ |  |  | stored-procedure |
| UserApplicationSetup |  | ✓ |  |  | stored-procedure |
| UserContact |  | ✓ |  |  | stored-procedure |
| UserDetails | ✓ |  |  |  | stored-procedure |
| WO |  | ✓ | ✓ |  | sql, stored-procedure |
| WODFileLog | ✓ |  |  |  | sql |
| WOHistory |  | ✓ |  |  | stored-procedure |

## Tier-B — unclassified stored procedures (no recognized entity/op)
- `dbo.prc_WOHistory_insert1` `[AI-SUGGESTED]`
- `dbo.sp_Application_Step_Status` `[AI-SUGGESTED]`
- `dbo.sp_BalanceStatementBankAccount_CreateAll` `[AI-SUGGESTED]`
- `dbo.sp_Create_Application_Steps` `[AI-SUGGESTED]`
- `dbo.sp_Create_Application_Steps_UpdateValid` `[AI-SUGGESTED]`
- `dbo.sp_StatementBankAccount_SetActive` `[AI-SUGGESTED]`

## Tier-B — entity lifecycle / states (inferred)
- Status-like fields suggest stateful entities: `InteremStatementType`, `StatementsFileRequired`, `WOStatusID_2`, `WOStatusID_4`, `WOStatusID_4_Flag` `[AI-SUGGESTED]`
