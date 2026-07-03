<template>
	<StadiumDataGrid
		:control-id="`Sample_SampleDataGrid`"
		:columnDefinitions="SampleDataGridColumnDefinitions"
		@Editclick="
		(doneCallback, ClickedRow) =>
			executeEvent({
				handler: () => SampleDataGrid_46Edit_46Click(ClickedRow),
				eventId: 'a79fc0c5-041f-4471-aefa-27d9be6b2172',
				doneCallback
			})
	"
	/>
</template>
<script>
export default {
	data() {
		return {
			SampleDataGridVisible: errorHandling.invoke(() => (typeResolver.toBoolean(true))),
			SampleDataGridColumnDefinitions: [
	{
		name: errorHandling.invoke(() => ('Edit')),
		classes: errorHandling.invoke(() => ('view-editimage')),
		headerText: errorHandling.invoke(() => (typeResolver.toString('Edit'))),
		hasClickEvent: true,
		visible: errorHandling.invoke(() => (true)),
		staticText: errorHandling.invoke(() => (typeResolver.toString(''))),
		cellAlignment: errorHandling.invoke(() => ('center'))
	},
	{
		name: errorHandling.invoke(() => ('Id')),
		classes: errorHandling.invoke(() => ('')),
		headerText: errorHandling.invoke(() => (typeResolver.toString('Id'))),
		hasClickEvent: false,
		visible: errorHandling.invoke(() => (false)),
		staticText: null,
		cellAlignment: errorHandling.invoke(() => ('left'))
	},
	{
		name: errorHandling.invoke(() => ('AccountName')),
		classes: errorHandling.invoke(() => ('')),
		headerText: errorHandling.invoke(() => (typeResolver.toString('Account Name'))),
		hasClickEvent: false,
		visible: errorHandling.invoke(() => (true)),
		staticText: null,
		cellAlignment: errorHandling.invoke(() => ('left'))
	}
]
		}
	},
	methods: {
		load() {
			return $stadiumRequest('api/Documents/Pages/Sample/SampleDataGrid_46Edit_46Click_46SampleUsersAPI_95UserGetById');
		},
		save() {
			return $stadiumRequest('api/Documents/Pages/Sample/SaveButton_46Click_46SampleCustomersAPI_95CustomerUpdate');
		}
	}
}
</script>
