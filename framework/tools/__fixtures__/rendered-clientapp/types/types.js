
export class _SampleUsersAPI_Types_UserRead_Roles_Type extends Array {
	_getItemTypeName() {
		return 'SampleUsersAPI_Types_Role';
	}
}


export class SampleUsersAPI_Types_Role {
	Id = undefined;
	Name = undefined;
	IsSystemRole = undefined;


}


export class SampleUsersAPI_Types_UserRead {
	Id = undefined;
	Email = undefined;
	FirstName = undefined;
	Roles = undefined;

	_getFieldTypeName(fieldName) {
		let customTypes = {
			Roles: '_SampleUsersAPI_Types_UserRead_Roles_Type'
		};

		return customTypes[fieldName];
	}
}


export class SampleUsersAPI_Types_UserWrite {
	Email = undefined;
	FirstName = undefined;
	Roles = undefined;

	_getFieldTypeName(fieldName) {
		let customTypes = {
			Roles: '_SampleUsersAPI_Types_UserRead_Roles_Type'
		};

		return customTypes[fieldName];
	}
}


export class SampleUsersAPI_Types_UserReadList {
	Users = undefined;


}


export class SampleCustomersAPI_Types_CustomerRead {
	Id = undefined;
	Name = undefined;


}


export class SampleCustomersAPI_Types_CustomerBasicRead {
	Id = undefined;


}


export class SampleCustomersAPI_Types_CustomerStatusRead {
	StatusId = undefined;
	StatusName = undefined;


}


export class SampleCustomersAPI_Types_GeneralError {
	Message = undefined;


}


export class SampleCustomersAPI_Types_ValidationResult {
	IsValid = undefined;


}


export class SampleCustomersAPI_Types_CustomerValidation {
	Field = undefined;


}


export class Types_Filter {
	Column = undefined;
	Operator = undefined;


}
