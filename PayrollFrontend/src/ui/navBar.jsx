import { NavLink } from "react-router-dom";

export default function NavBar() {
  return (
    <nav className="nav-container">
      <div className="navheader">
        <p>
          <b>User:</b> zahin
        </p>
        <p>
          <b>Department:</b> center
        </p>
      </div>
      <div className="links-container">
        <ul>
          <li>Home</li>
          <li>Departments</li>
          <li>
            <NavLink to="employee/list">Employees</NavLink>
          </li>
          <li>Payroll</li>
          <li>Employee Types</li>
          <li>
            <NavLink to="globalComponent/list">Global Components</NavLink>
          </li>
          <li>Loans</li>
          <li>Loan Requests</li>
          <li>Insurances</li>
          <li>Insurance Requests</li>
          <li>
            <NavLink to="users">Users</NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
}
