export default async function getEmployeeList({ token }) {
  const url = "http://127.0.0.1:8000/api/v1/employee/list/";
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
  });
  if (!response.ok) {
    throw Error("failed");
  }
  const data = await response.json();

  return data;
}
