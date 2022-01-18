import Card from 'components/card';
import DataTable from 'components/datatable';

export default function Index(){
  const baseUrl = '/employee/department';
  let renders = {
    col3: (data, row, dispatch) => {
      return <></>
    },

    col4: (data, row, dispatch) => {
      return <></>
    },
  };

  return (
    <Card
      title="Danh sách phòng ban"
      body={
        <DataTable 
          renders={renders}
          apiUrl={`${baseUrl}/search`}
        />
      }
    />
  )
}