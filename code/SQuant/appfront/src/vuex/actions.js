//应用mutation
export const setUser = ({commit},user) => {
  commit("userStatus",user)
}
export const setToken = ({commit},userToken) => {
  commit("userToken",userToken)
}
export const setType = ({commit},userType) => {
  commit("userType",userType)
}
  