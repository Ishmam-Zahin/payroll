import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";

import getEmployeeDetail from "../../helper/getEmployeeDetail";
import EmployeePhoto from "./employeePhoto";
import EmployeeEditButton from "./employeeEditButton";

export default function EmployeeDetail() {
  const token = useSelector((state) => state.userState.token);
  const { employeeId } = useParams();
  const { data, isError, isLoading, error } = useQuery({
    queryKey: ["employeeDetail"],
    queryFn: () => getEmployeeDetail({ token, employeeId }),
  });

  if (isLoading) {
    return <div>Loading</div>;
  }
  if (isError) {
    console.log(error);
    return <div>Failed</div>;
  }

  return (
    <div className="main-area">
      <h1 className="heading-center">
        Emplaoyee Details <EmployeeEditButton />
      </h1>
      <div className="employee-container">
        <EmployeePhoto employee={data} token={token} />
        <div className="employee-container__details">
          <p>
            {data["first_name"]} {data["last_name"]}
          </p>
          <p>
            <b>{data["employee_type"]},</b> <b>Grade: </b>
            {data["job_grade"]}
          </p>
          <p>
            <b>Department:</b> {data["department"]["full_name"]}
          </p>
          <p>
            <b>Gender</b>: {data["gender"]} <b>Relegion</b>: {data["relegion"]}
          </p>
          <p>
            <b>Phone: </b> {data["phone"]}
          </p>
          <p>
            <b>email: </b> {data["email"]}
          </p>
          <div className="leave-payroll-container">
            <p>
              <b>On Leave: </b>
              {data["on_leave"] ? "Yes" : "No"}
            </p>
            <p>
              <b>Calculate Payroll: </b>
              {data["payroll"] ? "Yes" : "No"}
            </p>
            <p>
              <b>Skip Loan: </b>
              {data["skip_loan"] ? "Yes" : "No"}
            </p>
            <p>
              <b>Main Payscale: </b> {data["basic_pay"]}
            </p>
          </div>
        </div>
      </div>
      <h2 className="heading-center table-heading">Global Components</h2>
      <div className="table-container">
        <div className="compensation-container">
          <h2>Compensations</h2>
          <table>
            <thead>
              <tr>
                <th>No</th>
                <th>Name</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {data["globalComponents"].map((obj, index) => {
                if (obj["component_type"] == "deduction") {
                  return null;
                }
                return (
                  <tr key={index}>
                    <td>0{index + 1}</td>
                    <td>{obj["global_component"]}</td>
                    <td>{obj["amount"]}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <div className="deduction-container">
          <h2>Deductions</h2>
          <table>
            <thead>
              <tr>
                <th>No</th>
                <th>Name</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {data["globalComponents"].map((obj, index) => {
                if (obj["component_type"] == "compensation") {
                  return null;
                }
                return (
                  <tr key={index}>
                    <td>0{index + 1}</td>
                    <td>{obj["global_component"]}</td>
                    <td>{obj["amount"]}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
      <h2 className="heading-center table-heading">
        Custom Components{" "}
        <button className="btn btn-green btn-small">Add New</button>
      </h2>
      <div className="table-container">
        <div className="compensation-container">
          <h2>Compensations</h2>
          <table>
            <thead>
              <tr>
                <th>No</th>
                <th>Name</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {data["globalComponents"].map((obj, index) => {
                if (obj["component_type"] == "deduction") {
                  return null;
                }
                return (
                  <tr key={index}>
                    <td>0{index + 1}</td>
                    <td>{obj["global_component"]}</td>
                    <td>{obj["amount"]}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <div className="deduction-container">
          <h2>Deductions</h2>
          <table>
            <thead>
              <tr>
                <th>No</th>
                <th>Name</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {data["globalComponents"].map((obj, index) => {
                if (obj["component_type"] == "compensation") {
                  return null;
                }
                return (
                  <tr key={index}>
                    <td>0{index + 1}</td>
                    <td>{obj["global_component"]}</td>
                    <td>{obj["amount"]}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
