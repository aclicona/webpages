import { GET_GROUPS } from '~/graphql/user'

export default function useGetGroups() {

  const { executeQuery } = useGraphQL()

  const grupos = async () => {
    const { getGruposList } = await executeQuery(GET_GROUPS)
    return getGruposList
  }
  return {
    grupos
  }
}