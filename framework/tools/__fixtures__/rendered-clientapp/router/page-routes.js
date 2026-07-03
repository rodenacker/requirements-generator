import Members from '@/views/Members.vue';
import MemberAdd from '@/views/MemberAdd.vue';
import MemberUpdate from '@/views/MemberUpdate.vue';

const pageRoutes = [
	{
	path: '/',
	redirect: '/Members'
},
{
	path: '/Members',
	component: Members,
	meta: { title: 'Members' }
},
{
	path: '/MemberAdd',
	component: MemberAdd,
	meta: { title: 'Member Add' }
},
{
	path: '/MemberUpdate',
	component: MemberUpdate,
	meta: { title: 'Member Update' }
}
];

export default pageRoutes;
