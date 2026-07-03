---
stadium_asset: data-sources
app: RMB_Onboarding
file_guid: 87ea91de-6125-4686-8437-806216cb0ec0
designer_version: 6.14.3378.13771
selected_package: 3f1ddf96-3519-47b8-905d-b44703776f78.sapz
extracted_from: C:\Stadium 6 Web Apps\87ea91de-6125-4686-8437-806216cb0ec0
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Data sources — RMB_Onboarding

> **Internal data-source contract — handoff-only.** The SQL / stored procedures / API endpoints below name the client's internal databases and services. Treat as backend-contract material, not prototype design input (only the payload *field names* in `data-model` are §7 shapes).

## Tier-A — connectors & operations

### OnboardingStandardBankCIB (Database)
- Connection (redacted): `{"$id": "3", "$type": "Twenty57.Stadium.API.ReferenceObjects.GuidReference, Twenty57.Stadium.API", "NamedItemID": "758e287d-90a8-4cbc-b0d1-060816733be2", "PropertyKey": null, "Parameters": {"$id": "4", "$type": "System.Collections.Generic.Dictionary`2[[System.Guid, System.Private.CoreLib],[System.Ob` [from administration.db / design model]
- **GetClients** (SqlQuery) — params: none [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT C.[ID] ,C.[CustomerName] FROM [tblCustomerDetails] C
  ```
- **GetCustomerInformation** (SqlQuery) — params: CustomerID:Int64 [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT TOP (1000) [ID] ,[CustomerName] ,[CustomerBaseCurrency] ,[CompanyTaxNumber] ,[CompanyVatNumber] ,[CompanyRegistrationNumber] ,[PasswordExpiryFrequency] ,[VATIndicator] ,[PreferredLanguage] ,[ContactPersonName] ,[ContactPersonSurame] ,[Email] ,[TelephoneNumber] ,[FaxNumber] FROM [tblCustomerDetails] WHERE ID = @CustomerID
  ```
- **UpdateCustomerInformation** (SqlQuery) — params: CustomerBaseCurrency:String, CompanyTaxNumber:String, CompanyVatNumber:String, CompanyRegistrationNumber:String, PasswordExpiryFrequency:String, VATIndicator:String, PreferredLanguage:String, ContactPersonName:String, ContactPersonSurame:String, TelephoneNumber:String, FaxNumber:String, CustomerID:String [from connector: OnboardingStandardBankCIB]
  ```sql
  UPDATE dbo.tblCustomerDetails SET CustomerBaseCurrency = @CustomerBaseCurrency ,CompanyTaxNumber = @CompanyTaxNumber ,CompanyVatNumber = @CompanyVatNumber ,CompanyRegistrationNumber = @CompanyRegistrationNumber ,PasswordExpiryFrequency = @PasswordExpiryFrequency ,VATIndicator = @VATIndicator ,PreferredLanguage = @PreferredLanguage ,ContactPersonName = @ContactPersonName ,ContactPersonSurame = @ContactPersonSurame ,TelephoneNumber = @TelephoneNumber ,FaxNumber = @FaxNumber WHERE ID = @CustomerID;
  ```
- **Sp_BankAccount_Insert** (StoredProcedure) — params: CustomerID:Int64, AccountName:AnsiString, BankName:AnsiString, BankAccountShortName:AnsiString, Currency:AnsiString, Country:AnsiString, BankAccountOwner:AnsiString, BankNumber:AnsiString, BankAccountStyle:AnsiString, BranchName:AnsiString, BicSwiftCode:AnsiString, BranchSortCode:AnsiString, IBAN:AnsiString, Serial:AnsiString, Success:Boolean, Message:AnsiString, ApplicationID:Int64 [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BankAccount_Insert`
- **Sp_BankAccount_Get** (StoredProcedure) — params: BankAccountID:Int64, Success:Boolean, Message:AnsiString, ApplicationID:Int64 [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BankAccount_Get`
- **Sp_BankAccount_Update** (StoredProcedure) — params: BankAccountID:Int64, AccountName:AnsiString, BankAccountShortName:AnsiString, Currency:AnsiString, Country:AnsiString, BankAccountStyle:AnsiString, BranchName:AnsiString, BicSwiftCode:AnsiString, BranchSortCode:AnsiString, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BankAccount_Update`
- **Sp_BankAccount_GetList** (StoredProcedure) — params: Success:Boolean, Message:AnsiString, ApplicationID:Int64 [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BankAccount_GetList`
- **Sp_UserDetails_GetList** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_UserDetails_GetList`
- **sql_ProductCurrencies_Get** (SqlQuery) — params: ProductId:String [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT TOP (1000) P.[ID] ,P.[CurrencyID] ,P.[ProductID] ,C.CurrencyName ,C.CurrencyCode FROM [tblProductCurrencies] P INNER JOIN tblCurrencyCode_ISO4217 C on C.ID = P.CurrencyID WHERE [ProductID] = @ProductId
  ```
- **sql_ProductCountries_Get** (SqlQuery) — params: ProductID:String [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT TOP (1000) P.[ID] ,P.[CountryID] ,P.[ProductID] ,C.Country FROM [tblProductCountries] P INNER JOIN tblCountryCode_ISO3166 C on C.ID = P.CountryID WHERE [ProductID] = @ProductID
  ```
- **Sp_BankAccount_Disable** (StoredProcedure) — params: BankAccountID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BankAccount_Disable`
- **Sp_CustomerDetails_Update** (StoredProcedure) — params: CustomerID:Int64, CustomerBaseCurrency:AnsiString, CompanyTaxNumber:AnsiString, CompanyVatNumber:AnsiString, CompanyRegistrationNumber:AnsiString, PasswordExpiryFrequency:Int16, VATIndicator:Boolean, PreferredLanguage:AnsiString, ContactPersonName:AnsiString, ContactPersonSurame:AnsiString, Email:AnsiString, TelephoneNumber:AnsiString, FaxNumber:AnsiString, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_CustomerDetails_Update`
- **Sp_Application_Create** (StoredProcedure) — params: CustomerID:Int64, CurrentStepID:Int64, WOID:Int32, ProductID:Int64, Success:Boolean, Message:AnsiString, ApplicationID:Int64, UserCreatedName:AnsiString, UserCreatedID:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Application_Create`
- **Prc_WO_Insert** (StoredProcedure) — params: WOTypeID_1:Int32, WOStatusID_2:Int32, WOPriorityID_3:Int32, NextActionSequence_4:Int32, NextActionDate_5:AnsiString, WOSource_6:Int32 [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.prc_WO_Insert`
- **Prc_WO_update** (StoredProcedure) — params: WOTypeID_3_Flag:Int32, WOStatusID_4_Flag:Int32, WOPriorityID_5_Flag:Int32, NextActionSequence_6_Flag:Int32, NextActionSequence_6_DefaultFlag:Int32, NextActionDate_7_Flag:Int32, WOSource_8_Flag:Int32, WOID_1:Int32, WOTypeID_3:Int32, WOStatusID_4:Int32, WOPriorityID_5:Int32, NextActionSequence_6:Int32, NextActionDate_7:AnsiString, WOSource_8:Int32 [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.prc_WO_update`
- **Prc_WOHistory_insert** (StoredProcedure) — params: WOID_1:Int32, WOActionID_2:Int32, WOActionNote_3:AnsiString, WOActionDate_4:AnsiString, WOActionUser_5:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.prc_WOHistory_insert`
- **Sp_User_Create** (StoredProcedure) — params: ApplicationID:Int64, UserName:AnsiString, UserMiddleName:AnsiString, UserSurname:AnsiString, IdentificationType:Int16, IdentificationNumber:AnsiString, Language:Int32, Gender:Int16, ReceiveCommunications:Boolean, ReceiveSMS:Boolean, ReceiveEmail:Boolean, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_User_Create`
- **Sp_Signatory_Create** (StoredProcedure) — params: ApplicationID:Int64, UserName:AnsiString, UserMiddleName:AnsiString, UserSurname:AnsiString, IdentificationType:Int16, IdentificationNumber:AnsiString, PassportNumber:AnsiString, DriversLicenceNumber:AnsiString, Success:Boolean, Message:AnsiString, UserID:Int64 [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Signatory_Create`
- **Sp_Signatories_GetList** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Signatories_GetList`
- **Sp_User_Update** (StoredProcedure) — params: UserID:Int64, ApplicationID:Int64, IdentificationType:Int16, IdentificationNumber:AnsiString, Language:Int32, Gender:Int16, ReceiveCommunications:Boolean, ReceiveSMS:Boolean, ReceiveEmail:Boolean, DateOfBirth:Date, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_User_Update`
- **Sp_Create_Application_Steps** (StoredProcedure) — params: ApplicationID:Int64, ProductID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Create_Application_Steps`
- **Sp_Create_Application_Steps_UpdateValid** (StoredProcedure) — params: ApplicationID:Int64, ProductID:Int64, StepNumber:Int32, StepIsValid:Boolean, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Create_Application_Steps_UpdateValid`
- **Sp_Application_Steps_Get** (StoredProcedure) — params: ApplicationID:Int64, ProductID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Application_Steps_Get`
- **Sp_BalanceStatementBankAccount_Insert** (StoredProcedure) — params: ApplicationID:Int64, BankAccountID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BalanceStatementBankAccount_Insert`
- **Sp_Application_GetList** (StoredProcedure) — params: Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Application_GetList`
- **sqlTypeItems_Get** (SqlQuery) — params: CfgTypeID:Int64 [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT ID ,CfgTypeID ,TypeID ,Name ,Description FROM dbo.tblCfgTypeItems WHERE CfgTypeID = @CfgTypeID
  ```
- **Sp_BalanceHostToHost_Insert** (StoredProcedure) — params: ApplicationID:Int64, ScheduleName:AnsiString, StatementsFileRequired:Int32, SortTransactionsOnDate:Int32, InteremStatementType:Int32, TimeFrom:Time, TimeTo:Time, RepeatEvery:Int32, Success:Boolean, Message:AnsiString, Daily:Boolean, Monday:Boolean, Tuesday:Boolean, Wedenesday:Boolean, Thursday:Boolean, Friday:Boolean, Saturday:Boolean, Sunday:Boolean [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BalanceHostToHost_Insert`
- **Sp_BalanceSetup_Insert** (StoredProcedure) — params: ApplicationID:Int64, ProductsAccountBalances:Boolean, Movement:Boolean, ConsolidatedBalances:Boolean, AccountGroup:Boolean, AccountSubGroup:Boolean, HostToHost:Boolean, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BalanceSetup_Insert`
- **Sp_BalanceStatementBankAccount_GetList** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BalanceStatementBankAccount_GetList`
- **Sp_BalanceStatementBankAccount_CreateAll** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BalanceStatementBankAccount_CreateAll`
- **Sp_BalanceStatementBankAccount_Delete** (StoredProcedure) — params: ApplicationID:Int64, ID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_BalanceStatementBankAccount_Delete`
- **sql_UserCount_Get** (SqlQuery) — params: ApplicationID:Int64 [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT Count(ID) as [Count] FROM [dbo].[tblUserDetails] WHERE ApplicationID = @ApplicationID
  ```
- **Sp_ClientApplications_Get** (StoredProcedure) — params: Success:Boolean, Message:AnsiString, UserAllocated:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_ClientApplications_Get`
- **Sp_ClientApplicationsUnallocated_Get** (StoredProcedure) — params: Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_ClientApplicationsUnallocated_Get`
- **Sp_ClientApplications_Allocate_Insert** (StoredProcedure) — params: ApplicationID:Int64, UserName:AnsiString, UserGuid:AnsiString, UserEmail:AnsiString, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_ClientApplications_Allocate_Insert`
- **Sp_ApplicationDocument_Get** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_ApplicationDocument_Get`
- **Sp_Product_PaymentsAndFeatures_Insert** (StoredProcedure) — params: ApplicationID:Int64, ManageOrders:Boolean, ReRelease:Boolean, ViewBeneficiaryDetail:Boolean, MyBills:Boolean, BillsSARSDOL:Boolean, ThirdPartyPayment:Boolean, PayAlert:Boolean, CreditFacility:Boolean, ViewLimits:Boolean, EarlyClearingValidation:Boolean, AvailableFundsCheck:Boolean, RecurringPayments:Boolean, AdhocBOPThirdParty:Boolean, ViewAvailableBalance:Boolean, PostingType:Int32, PostingItemised:Boolean, PostingConsolidated:Boolean, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Product_PaymentsAndFeatures_Insert`
- **Sp_Product_ServiceSetup_Insert** (StoredProcedure) — params: ApplicationID:Int64, Beneficiary:Boolean, PayAlert:Boolean, AuthoriseOwnBeneficiary:Boolean, PaymentType:Boolean, BOPThirdParty:Boolean, Biller:Boolean, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Product_ServiceSetup_Insert`
- **Sp_Product_AdminSetup_Insert** (StoredProcedure) — params: ApplicationID:Int64, Normal:Boolean, Urgent:Boolean, SynchronisedPayment:Boolean, ValueDated:Boolean, Instant:Boolean, Mobile:Boolean, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Product_AdminSetup_Insert`
- **Sp_History_Get** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_History_Get`
- **Sp_Application_Step_Status** (StoredProcedure) — params: ApplicationID:Int64, StepID:Int64, IsValid:Boolean, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Application_Step_Status`
- **sql_GetProvincesFromCountry** (SqlQuery) — params: CountryID:String [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT TOP (100) [ID] ,[CountryID] ,[ProviceName] FROM [tblCountryProvinces] WHERE CountryID = @CountryID
  ```
- **sql_GetApplicationFile** (SqlQuery) — params: ApplicationID:String [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT TOP 1 a.ID, a.WOID, FileName, FileLocation, CFFileSettingID FROM WODFileLog fl JOIN tblApplications a ON a.WOID = fl.WOID WHERE CFFileSettingID = 8 AND fl.WOID = a.WOID AND a.ID = @ApplicationID ORDER BY WODFileLogID DESC
  ```
- **sql_ApplicationUpdateEmail** (SqlQuery) — params: ApplicationEmail:String, ApplicationID:String [from connector: OnboardingStandardBankCIB]
  ```sql
  UPDATE dbo.tblApplications SET ApplicationEmail = @ApplicationEmail WHERE ID = @ApplicationID
  ```
- **Sp_Signatory_SigningArrangements_Insert** (StoredProcedure) — params: ApplicationID:Int64, Joint:Boolean, SignatoryCount:Int16, Severally:Boolean, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Signatory_SigningArrangements_Insert`
- **Sp_Signatory_SigningArrangements_Get** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Signatory_SigningArrangements_Get`
- **Sp_StatementBankAccount_SetActive** (StoredProcedure) — params: BankAccountID:Int64, ApplicationID:Int64, Active:Boolean, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_StatementBankAccount_SetActive`
- **Sp_User_Disable** (StoredProcedure) — params: ApplicationID:Int64, UserID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_User_Disable`
- **Sp_UserAddress_Insert** (StoredProcedure) — params: UserID:Int64, PhysicalAddress:AnsiString, Suburb:AnsiString, City:AnsiString, Province:AnsiString, ProvinceID:Int16, CountryId:Int16, PostalCode:AnsiString, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_UserAddress_Insert`
- **Sp_UserApplicationSetup_Insert** (StoredProcedure) — params: UserID:Int64, SignatoryType:Int16, DesignatedPerson:Boolean, EmailNotificationsOnAuthorisation:Boolean, StartDate:Date, EndDate:Date, StartEndDateAvailable:Boolean, SelfServiceAdministrator:Boolean, ResetOwnPassword:Boolean, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_UserApplicationSetup_Insert`
- **Sp_UserContact_Insert** (StoredProcedure) — params: UserID:Int64, TelephoneNumber:AnsiString, AlternativeTelephoneNumber:AnsiString, MobileNumber:AnsiString, FaxNumber:AnsiString, EmailAddress:AnsiString, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_UserContact_Insert`
- **Sp_SignatoryAddress_Insert** (StoredProcedure) — params: SignatoryID:Int64, PhysicalAddress:AnsiString, Suburb:AnsiString, City:AnsiString, Province:AnsiString, ProvinceID:Int16, CountryId:Int16, PostalCode:AnsiString, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_SignatoryAddress_Insert`
- **Sp_Signatories_Disable** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString, SignatoryID:Int64 [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Signatories_Disable`
- **Sp_Signatories_UserDisabled_Disable** (StoredProcedure) — params: ApplicationID:Int64, UserID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_Signatories_UserDisabled_Disable`
- **GetSignatoryCount** (SqlQuery) — params: ApplicationID:String [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT Count([ID]) AS [COUNT] FROM [dbo].[tblSignatories] S WHERE S.ApplicationID = @ApplicationID AND S.Active = 1
  ```
- **GetBankAccountCount** (SqlQuery) — params: ApplicationID:String [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT Count([ID]) as [Count] FROM [dbo].[tblBankAccount] WHERE [ApplicationID] = @ApplicationID AND Active = 1
  ```
- **Sp_User_Get** (StoredProcedure) — params: ApplicationID:Int64, UserID:Int64, Success:Boolean, Message:AnsiString [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_User_Get`
- **Get_StatusCount** (SqlQuery) — params: none [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT W.NextActionSequence, COUNT(*) FROM tblApplications A INNER JOIN WO W on W.WOID = A.WOID GROUP BY W.NextActionSequence;
  ```
- **Sp_FileImage_Get** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString, Count:Int32 [from connector: OnboardingStandardBankCIB]
  - proc: `dbo.sp_FileImage_Get`
- **sql_GetApplciationWOID** (SqlQuery) — params: ApplicationID:String [from connector: OnboardingStandardBankCIB]
  ```sql
  SELECT WOID FROM dbo.tblApplications WHERE ID = @ApplicationID
  ```
- **Query** (SqlQuery) — params: none [from connector: OnboardingStandardBankCIB]

### Stadium (WebService)
- Connection (redacted): `{"URL": "http://localhost:8047/", "Auth": "Anonymous", "Timeout": 90}` [from administration.db / design model]
- **Clients** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: Stadium]
  - endpoint: `GET /v1/Clients`
- **ClientsAndProducts** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: Stadium]
  - endpoint: `GET /v1/ClientsAndProducts`

### FileSystem (FileSystem)
- Connection (redacted): `{"Path": "C:\\Digiata\\Digiata_Demo\\Data\\Inbox\\Applications", "User": "", "Password": ""}` [from administration.db / design model]
- **DeleteFile** (DeleteFile) — params: FileName:Parameter [from connector: FileSystem]
- **FileExists** (FileExists) — params: FileName:Parameter [from connector: FileSystem]
- **ReadFile** (ReadFile) — params: FileName:Parameter [from connector: FileSystem]
- **WriteFile** (WriteFile) — params: FileName:Parameter, FileContents:Parameter [from connector: FileSystem]

### FileSystemDemo (FileSystem)
- Connection (redacted): `{"Path": "C:\\Digiata\\Digiata_Demo\\Data\\Outbox\\Applications", "User": "", "Password": ""}` [from administration.db / design model]
- **DeleteFile** (DeleteFile) — params: FileName:Parameter [from connector: FileSystemDemo]
- **FileExists** (FileExists) — params: FileName:Parameter [from connector: FileSystemDemo]
- **ReadFile** (ReadFile) — params: FileName:Parameter [from connector: FileSystemDemo]
- **WriteFile** (WriteFile) — params: FileName:Parameter, FileContents:Parameter [from connector: FileSystemDemo]

### FileSystemData (FileSystem)
- Connection (redacted): `{"Path": "C:\\Digiata\\Digiata_Demo\\Data", "User": "", "Password": ""}` [from administration.db / design model]
- **DeleteFile** (DeleteFile) — params: FileName:Parameter [from connector: FileSystemData]
- **FileExists** (FileExists) — params: FileName:Parameter [from connector: FileSystemData]
- **ReadFile** (ReadFile) — params: FileName:Parameter [from connector: FileSystemData]
- **WriteFile** (WriteFile) — params: FileName:Parameter, FileContents:Parameter [from connector: FileSystemData]

### IDB (Database)
- Connection (redacted): `Data Source=.\;Initial Catalog=IDB;Integrated Security=False;User ID=LINX_SERVER;Password=<redacted>;Trust Server Certificate=true;` [from administration.db / design model]
- **get_AllClientDetails** (SqlQuery) — params: none [from connector: IDB]
  ```sql
  SELECT * FROM dbo.tbl_ClientDetails
  ```
- **get_ClientDetails** (SqlQuery) — params: ClientID:String [from connector: IDB]
  ```sql
  SELECT ClientName, ClientRegistrationNumber FROM dbo.tbl_ClientDetails WHERE _ClientIDinternal = @ClientID
  ```
- **Prc_ClientDetails_Insert** (StoredProcedure) — params: ClientName:AnsiString, ClientSurname:AnsiString, ClientID:AnsiString, ClientRegistrationNumber:AnsiString, ClientSegment:AnsiString [from connector: IDB]
  - proc: `dbo.prc_ClientDetails_Insert`
- **Prc_WO_Insert_1** (StoredProcedure) — params: WOTypeID_1:Int32, WOStatusID_2:Int32, WOPriorityID_3:Int32, NextActionSequence_4:Int32, NextActionDate_5:AnsiString, WOSource_6:Int32, WOID:Int32 [from connector: IDB]
  - proc: `dbo.prc_WO_Insert_ReturnWOID`
- **Prc_Application_Insert** (StoredProcedure) — params: WOID:Int32, ClientID:Int32, UserCreatedName:AnsiString, UserCreatedID:AnsiString [from connector: IDB]
  - proc: `dbo.prc_Application_Insert`
- **get_CheckModularInformationExists** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  DECLARE @ModularInformationExists int IF EXISTS (SELECT 1 FROM dbo.tbl_ModularForm WHERE _ApplicationID = @ApplicationID) SET @ModularInformationExists = 1 ELSE SET @ModularInformationExists = 0 SELECT @ModularInformationExists AS [ModularInformationExists]
  ```
- **get_ModularInformation** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  SELECT * FROM tbl_ModularForm WHERE _ApplicationID = @ApplicationID
  ```
- **Prc_ModularInformation_Insert** (StoredProcedure) — params: ModularNominatedAccountPayments:Int32, ModularOnceOffPayments:Boolean, ModularTransfers:Boolean, ModularCollections:Boolean, ModularAandBSignatories:Boolean, ModularCashman:Boolean, ModularLinkCCNNumber1:AnsiString, ModularLinkCCNNumber2:AnsiString, ModularLinkCCNNumber3:AnsiString, ModularLinkCCNNumber4:AnsiString, ModularLinkCCNNumber5:AnsiString, ModularLinkCCNNumber6:AnsiString, ModularCashmanReports:Boolean, ModularNAEDO:Boolean, ModularOnlineSettlementLimits:Boolean, ModularFTPDeliveryMechanism:Boolean, _ApplicationID:Int32 [from connector: IDB]
  - proc: `dbo.prc_ModularInformation_Insert`
- **Prc_ModularInformation_Update** (StoredProcedure) — params: ModularNominatedAccountPayments:Int32, ModularOnceOffPayments:Boolean, ModularTransfers:Boolean, ModularCollections:Boolean, ModularAandBSignatories:Boolean, ModularCashman:Boolean, ModularLinkCCNNumber1:AnsiString, ModularLinkCCNNumber2:AnsiString, ModularLinkCCNNumber3:AnsiString, ModularLinkCCNNumber4:AnsiString, ModularLinkCCNNumber5:AnsiString, ModularLinkCCNNumber6:AnsiString, ModularCashmanReports:Boolean, ModularNAEDO:Boolean, ModularOnlineSettlementLimits:Boolean, ModularFTPDeliveryMechanism:Boolean, ApplicationID:Int32 [from connector: IDB]
  - proc: `dbo.prc_ModularInformation_Update`
- **get_ModularEntities** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  SELECT _ModEntityID ,ModEntityName ,ModEntityNumber ,_ModularID FROM dbo.tbl_ModularFormEntityTable WHERE _ModularID = (SELECT _ModularID FROM tbl_ModularForm WHERE _ApplicationID = @ApplicationID)
  ```
- **Prc_ModularEntity_Insert** (StoredProcedure) — params: ModEntityName:AnsiString, ModEntityNumber:AnsiString, ApplicationID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_ModularEntity_Insert`
- **Prc_ModularEntity_Update** (StoredProcedure) — params: ModEntityName:AnsiString, ModEntityNumber:AnsiString, ModEntityID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_ModularEntity_Update`
- **get_ModularEntity** (SqlQuery) — params: ModularEntityID:String [from connector: IDB]
  ```sql
  SELECT _ModEntityID ,ModEntityName ,ModEntityNumber ,_ModularID FROM dbo.tbl_ModularFormEntityTable WHERE _ModEntityID = @ModularEntityID
  ```
- **Prc_ModularEntity_GetList** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_ModularEntity_GetList`
- **get_SectionValidationStatus** (SqlQuery) — params: none [from connector: IDB]
  ```sql
  SELECT 'Modular Information','Passed' UNION SELECT 'Collections Application', 'Passed' UNION SELECT 'Appointment of Administrators', 'Passed' UNION SELECT 'Subgroups', 'Passed' UNION SELECT 'Signatories', 'Passed'
  ```
- **get_CheckCollectionsExists** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  DECLARE @CollectionsExists int IF EXISTS (SELECT 1 FROM dbo.tbl_CollectionsApplication WHERE _ApplicationID = @ApplicationID) SET @CollectionsExists = 1 ELSE SET @CollectionsExists = 0 SELECT @CollectionsExists AS [CollectionsExists]
  ```
- **get_Collections** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  SELECT _CollectionsApplicationID ,CollAppClientName ,CollAppAccountNumber ,CollAppBranchCode ,_ApplicationID FROM dbo.tbl_CollectionsApplication WHERE _ApplicationID = @ApplicationID
  ```
- **Prc_Collections_Insert** (StoredProcedure) — params: CollAppClientName:AnsiString, CollAppAccountNumber:AnsiString, CollAppBranchCode:AnsiString, ApplicationID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_Collections_Insert`
- **Prc_Collections_Update** (StoredProcedure) — params: CollAppClientName:AnsiString, CollAppAccountNumber:AnsiString, CollAppBranchCode:AnsiString, ApplicationID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_Collections_Update`
- **Prc_CollectionsContactPerson_Insert** (StoredProcedure) — params: ContPAbbreviatedName:AnsiString, ContPAccountNumber:AnsiString, ContPCompanyName:AnsiString, ContPContactName:AnsiString, ContPContactTelNo:AnsiString, ContPContactEmail:AnsiString, ApplicationID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_CollectionsContactPerson_Insert`
- **Prc_CollectionsContactPerson_Update** (StoredProcedure) — params: ContPAbbreviatedName:AnsiString, ContPAccountNumber:AnsiString, ContPCompanyName:AnsiString, ContPContactName:AnsiString, ContPContactTelNo:AnsiString, ContPContactEmail:AnsiString, ContactPersonID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_CollectionsContactPerson_Update`
- **Prc_CollectionsContactPerson_GetList** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_CollectionsContactPerson_GetList`
- **get_CollectionsContactPerson** (SqlQuery) — params: ContactPersonID:String [from connector: IDB]
  ```sql
  SELECT _ContactPersonID ,ContPAbbreviatedName ,ContPAccountNumber ,ContPCompanyName ,ContPContactName ,ContPContactTelNo ,ContPContactEmail ,_CollectionsApplicationID FROM dbo.tbl_CollectionsContactPerson WHERE _ContactPersonID = @ContactPersonID
  ```
- **get_Administrator** (SqlQuery) — params: AdministratorID:String [from connector: IDB]
  ```sql
  SELECT _AdminID ,AdminFullName ,AdminID_Passport ,AdminCapacity ,_ApplicationID ,IDType FROM dbo.tbl_AppointmentOfAdmins WHERE _AdminID = @AdministratorID
  ```
- **get_CheckAdministratorsExist** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  DECLARE @AdministratorsExists int IF EXISTS (SELECT 1 FROM dbo.tbl_AppointmentOfAdmins WHERE _ApplicationID = @ApplicationID) SET @AdministratorsExists = 1 ELSE SET @AdministratorsExists = 0 SELECT @AdministratorsExists AS [AdministratorsExists]
  ```
- **Prc_Administrators_GetList** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_Administrators_GetList`
- **Prc_Administrators_Insert** (StoredProcedure) — params: AdminFullName:AnsiString, AdminID_Passport:AnsiString, AdminCapacity:AnsiString, ApplicationID:Int32, Success:Boolean, Message:AnsiString, IDType:Int16 [from connector: IDB]
  - proc: `dbo.prc_Administrators_Insert`
- **Prc_Administrators_Update** (StoredProcedure) — params: AdminFullName:AnsiString, AdminID_Passport:AnsiString, AdminCapacity:AnsiString, AdministratorsID:Int32, Success:Boolean, Message:AnsiString, IDType:Int16 [from connector: IDB]
  - proc: `dbo.prc_Administrators_Update`
- **get_HeirarchyEntities** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  SELECT _HeirarchyEntitiesID ,EntityName ,EntityNumber ,_ApplicationID FROM dbo.tbl_HeirarchyEntities WHERE _ApplicationID = @ApplicationID
  ```
- **get_CheckHeirarchyEntitiesExists** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  DECLARE @HeirarchyEntitiesExists int IF EXISTS (SELECT 1 FROM dbo.tbl_HeirarchyEntities WHERE _ApplicationID = @ApplicationID) SET @HeirarchyEntitiesExists = 1 ELSE SET @HeirarchyEntitiesExists = 0 SELECT @HeirarchyEntitiesExists AS [HeirarchyEntitiesExists]
  ```
- **sp_Application_Step_Status** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString, StepID:Int64, IsValid:Boolean [from connector: IDB]
  - proc: `dbo.sp_Application_Step_Status`
- **sp_Application_Steps_Get** (StoredProcedure) — params: ApplicationID:Int64, ProductID:Int64, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.sp_Application_Steps_Get`
- **sp_Create_Application_Steps** (StoredProcedure) — params: WOID:Int64, ProductID:Int64, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.sp_Create_Application_Steps`
- **sp_Create_Application_Steps_UpdateValid** (StoredProcedure) — params: WOID:Int64, ProductID:Int64, StepNumber:Int32, StepIsValid:Boolean, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.sp_Create_Application_Steps_UpdateValid`
- **Prc_WO_Update** (StoredProcedure) — params: WOTypeID_3_Flag:Int32, WOStatusID_4_Flag:Int32, WOPriorityID_5_Flag:Int32, NextActionSequence_6_Flag:Int32, NextActionSequence_6_DefaultFlag:Int32, NextActionDate_7_Flag:Int32, WOSource_8_Flag:Int32, WOID_1:Int32, WOTypeID_3:Int32, WOStatusID_4:Int32, WOPriorityID_5:Int32, NextActionSequence_6:Int32, NextActionDate_7:AnsiString, WOSource_8:Int32 [from connector: IDB]
  - proc: `dbo.prc_WO_update`
- **Prc_WOHistory_insert1** (StoredProcedure) — params: WOID_1:Int32, WOActionID_2:Int32, WOActionNote_3:AnsiString, WOActionDate_4:AnsiString, WOActionUser_5:AnsiString [from connector: IDB]
  - proc: `dbo.prc_WOHistory_insert1`
- **Prc_CollectionsContactPerson_Disable** (StoredProcedure) — params: ContactPersonID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_CollectionsContactPerson_Disable`
- **Prc_Administrators_Disable** (StoredProcedure) — params: AdministratorsID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_Administrators_Disable`
- **Prc_PartiesHeirarchy_Disable** (StoredProcedure) — params: PartiesHeirarchyID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_PartiesHeirarchy_Disable`
- **Prc_PartiesHeirarchy_GetList** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_PartiesHeirarchy_GetList`
- **Prc_PartiesHeirarchy_HeirarchyEntitiesID_Update** (StoredProcedure) — params: PartiesHeirarchyID:Int32, HeirarchyEntitiesID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_PartiesHeirarchy_HeirarchyEntitiesID_Update`
- **Prc_PartiesHeirarchy_Insert** (StoredProcedure) — params: PartiesHAccountName:AnsiString, PartiesHAccountNumber:AnsiString, HeirarchyEntitiesID:AnsiString, ApplicationID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_PartiesHeirarchy_Insert`
- **Prc_PartiesHeirarchy_Update** (StoredProcedure) — params: Success:Boolean, Message:AnsiString, PartiesHeirarchyID:Int32, PartiesHAccountName:AnsiString, PartiesHAccountNumber:AnsiString, HeirarchyEntitiesID:Int32 [from connector: IDB]
  - proc: `dbo.prc_PartiesHeirarchy_Update`
- **get_EntitiesExist** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  DECLARE @EntitiesExists int IF EXISTS (SELECT 1 FROM dbo.tbl_HeirarchyEntities WHERE _ApplicationID = @ApplicationID) SET @EntitiesExists = 1 ELSE SET @EntitiesExists = 0 SELECT @EntitiesExists AS [EntitiesExists]
  ```
- **Prc_HeirarchyEntities_Insert** (StoredProcedure) — params: EntityName:AnsiString, EntityNumber:AnsiString, ApplicationID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_HeirarchyEntities_Insert`
- **Prc_HeirarchyEntities_Update** (StoredProcedure) — params: EntityName:AnsiString, EntityNumber:AnsiString, ApplicationID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_HeirarchyEntities_Update`
- **get_AdministratorCount** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  SELECT Count(*) as Count FROM dbo.tbl_AppointmentOfAdmins WHERE _ApplicationID = @ApplicationID AND Enabled = 1
  ```
- **get_ContactPersonCount** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  SELECT Count(*) as Count FROM dbo.tbl_CollectionsContactPerson WHERE _ApplicationID = @ApplicationID AND Enabled = 1
  ```
- **get_PartiesHierarchCount** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  SELECT Count(*) as Count FROM dbo.tbl_PartiesHeirarchyTable WHERE _ApplicationID = @ApplicationID AND Enabled = 1
  ```
- **get_PartiesHeirarchyTable** (SqlQuery) — params: PartiesHeirarchyID:String [from connector: IDB]
  ```sql
  SELECT [_PartiesHeirarchyID] ,[PartiesHAccountName] ,[PartiesHAccountNumber] ,[_HeirarchyEntitiesID] ,[_ApplicationID] ,[Enabled] FROM [IDB].[dbo].[tbl_PartiesHeirarchyTable] WHERE [_PartiesHeirarchyID] = @PartiesHeirarchyID
  ```
- **Prc_Signatories_Update** (StoredProcedure) — params: SignatureFullNameSurname:AnsiString, SignatureDesignation:AnsiString, SignatureIDPassport:AnsiString, SignatureInitials:AnsiString, IDType:Int16, SignatureFieldID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_Signatories_Update`
- **Prc_SignatureField_Disable** (StoredProcedure) — params: SignatureFieldID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_SignatureField_Disable`
- **Prc_SignatureField_GetList** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_SignatureField_GetList`
- **Prc_SignatureField_Insert** (StoredProcedure) — params: SignatureFullNameSurname:AnsiString, SignatureDesignation:AnsiString, SignatureIDPassport:AnsiString, SignatureInitials:AnsiString, IDType:Int16, ApplicationID:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_SignatureField_Insert`
- **get_SignatoryCount** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  SELECT Count(*) as Count FROM dbo.tbl_SignatureField WHERE _ApplicationID = @ApplicationID AND Enabled = 1
  ```
- **get_Signatory** (SqlQuery) — params: SignatoryID:String [from connector: IDB]
  ```sql
  SELECT [_SignatureFieldID] ,[SignatureFullNameSurname] ,[SignatureDesignation] ,[SignatureIDPassport] ,[SignatureInitials] ,[_ApplicationID] ,[IDType] ,[Enabled] FROM [dbo].[tbl_SignatureField] WHERE [_SignatureFieldID] = @SignatoryID
  ```
- **get_InvalidSteps** (SqlQuery) — params: WOID:String [from connector: IDB]
  ```sql
  SELECT Count(*) as Count FROM [IDB].[dbo].[tblApplicationSteps] WHERE WOID = @WOID AND StepValid = 0
  ```
- **Prc_Application_GetAll** (StoredProcedure) — params: Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.prc_Application_GetAll`
- **Sp_History_Get** (StoredProcedure) — params: ApplicationID:Int64, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.sp_History_Get`
- **Sp_ClientApplications_Get** (StoredProcedure) — params: UserAllocated:AnsiString, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.sp_ClientApplications_Get`
- **Sp_ClientApplicationsUnallocated_Get** (StoredProcedure) — params: UserAllocated:AnsiString, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.sp_ClientApplicationsUnallocated_Get`
- **get_ApplicationFile** (SqlQuery) — params: ApplicationID:String [from connector: IDB]
  ```sql
  SELECT TOP 1 a._ApplicationID, a.WOID, FileName, FileLocation, CFFileSettingID FROM WODFileLog fl JOIN tbl_ApplicationForRMB a ON a.WOID = fl.WOID WHERE CFFileSettingID = 8 AND fl.WOID = a.WOID AND a._ApplicationID = @ApplicationID ORDER BY WODFileLogID DESC
  ```
- **Query** (SqlQuery) — params: none [from connector: IDB]
- **Sp_FileImage_Get** (StoredProcedure) — params: ApplicationID:Int64, Count:Int32, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.sp_FileImage_Get`
- **Sp_ClientApplications_Allocate_Insert** (StoredProcedure) — params: ApplicationID:Int64, UserName:AnsiString, UserGuid:AnsiString, UserEmail:AnsiString, Success:Boolean, Message:AnsiString [from connector: IDB]
  - proc: `dbo.sp_ClientApplications_Allocate_Insert`

## Tier-A — app settings / integration

- Config value present: `MenuItems` (structured/large value, not shown) [from design model: Setting]
