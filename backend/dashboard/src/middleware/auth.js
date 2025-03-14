import userLogin from "../plugins/user/login";


const auth = async ({next, router}) => {
    const userIsLogin = await userLogin.isLogged
    if (!userIsLogin) {
        return router.push({name: 'login'});
    }
    return next();
}
export {auth}