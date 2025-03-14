import { gql } from '@apollo/client/core'

const GROUP_INPUT = gql`
    input GroupInput {
        name: String!
        add: Boolean!
    }
`
const ME_QUERY = gql`
    query Me {
        me {
            id
            email
            firstName
            lastName
            avatar
            image
        }
    }`
const USER_IS_LOGGED = gql`
    query authenticated {
        authenticated
    }`

const LOGIN = gql`
    mutation loginAuthToken($email: String!, $password: String!){
        loginAuthToken(email:$email, password: $password){
            success
            errors
            token {
                token
            }
            refreshToken{
                token
            }
        }
    }
`
const REGISTER_USER = gql`
    mutation registerUser($email: String!, $password: String!, $firstName: String!){
        registerUser(
            email: $email
            password1: $password
            password2: $password
            firstName: $firstName)
        {
            success
            errors
        }
    }
`
const GRUPOS_USUARIOS = gql`
    query{
        getGruposUsuario
    }
`
const LOGOUT = gql`
    mutation logoutUser{
        logoutUser{
            success
            message
            errors
        }
    }
`
const RESEND_ACTIVATION_EMAIL = gql`
    mutation resendActivationEmail($email: String!){
        resendActivationEmail(email: $email){
            success,
            errors
        }
    }
`
const PASSWORD_RESET = gql`
    mutation passwordReset($token: String!, $password:String!){
        passwordReset(token: $token, newPassword1: $password, newPassword2: $password) {
            success,
            errors
        }
    }
`
const PASSWORD_CHANGE = gql`
    mutation passwordChange($oldPassword: String!, $newPassword:String!){
        passwordChange(oldPassword: $oldPassword, newPassword1: $newPassword, newPassword2: $newPassword) {
            success,
            errors,
            refreshToken{
                token
            }
        }
    }
`
const PASSWORD_RESET_EMAIL = gql`
    mutation sendPasswordResetEmail($email: String!){
        sendPasswordResetEmail(email: $email){
            success,
            errors
        }
    }
`
const USER_STAFF_CREATION = gql`
    mutation createStaffUser($email: String!, $firstName: String!, $lastName: String, $groups:[GroupInput!]!){
        createStaffUser(input:{email: $email, firstName: $firstName, lastName: $lastName, groups: $groups}){
            success
        }
    }
`
const GET_GROUPS = gql`
    query getGruposList{
        getGruposList
    }
`
const REFRESH_TOKEN = gql`mutation ($refreshToken:String!){
    refreshToken(
        refreshToken: $refreshToken,
        revokeRefreshToken:false
    ) {
        success,
        errors,
        token{
            token
        }
    }
}
`
const VERIFY_ACCOUNT = gql`
    mutation verifyAccount($token: String!){
        verifyAccount(token: $token){
            success,
            errors
        }
    }
`
export {
  LOGIN, ME_QUERY, REGISTER_USER, LOGOUT, GRUPOS_USUARIOS, USER_IS_LOGGED,
  RESEND_ACTIVATION_EMAIL, PASSWORD_RESET, PASSWORD_CHANGE, PASSWORD_RESET_EMAIL,
  USER_STAFF_CREATION, GET_GROUPS, REFRESH_TOKEN, VERIFY_ACCOUNT
}