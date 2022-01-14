import Login from "pages/login";
import Signup from "pages/signup";
import Reception from "pages/reception";
import PendingVisit from "pages/encounter/pending";
import CompleteVisit from "pages/encounter/complete";
import RolePage from "pages/system/account/role";
import UserPage from "pages/system/account/user";

import { 
  Routes, 
  Route, 
  Link, 
  withRouter, 
  useLocation, 
  useNavigate 
} from "react-router-dom";

export default function App() {
  const navigate = useNavigate();
  const loc = useLocation();
  const loggedIn = localStorage.getItem('token');
  const pathname = loc.pathname;
  
  if(!loggedIn) {
    if(pathname === '/signup') {
      return <Signup/>;
    }else {
      return <Login/>;
    }
  }

  return (
    <>
      <nav className="sb-topnav navbar navbar-expand navbar-dark bg-dark">
        <Link className="navbar-brand ps-3" to="/">EMR</Link>
        <button className="btn btn-link btn-sm order-1 order-lg-0 me-4 me-lg-0" id="sidebarToggle" href="#!"><i
          className="fas fa-bars"></i></button>
        <form className="d-none d-md-inline-block form-inline ms-auto me-0 me-md-3 my-2 my-md-0">
          <div className="input-group">
            <input className="form-control" type="text" placeholder="Tìm kiếm..."
              aria-describedby="btnNavbarSearch" />
            <button className="btn btn-primary" id="btnNavbarSearch" type="button"><i className="fas fa-search"></i></button>
          </div>
        </form>
        <ul className="navbar-nav ms-auto ms-md-0 me-3 me-lg-4">
          <li className="nav-item dropdown">
            <a className="nav-link dropdown-toggle" id="navbarDropdown" href="#" role="button" data-bs-toggle="dropdown"
              aria-expanded="false"><i className="fas fa-user fa-fw"></i></a>
            <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
              <li><a className="dropdown-item" href="#!">Cài đặt</a></li>
              <li><a className="dropdown-item" href="#!">Thông tin tài khoản</a></li>
              <li>
                <hr className="dropdown-divider" />
              </li>
              <li><a className="dropdown-item" href="#!">Đăng xuất</a></li>
            </ul>
          </li>
        </ul>
      </nav>
      <div id="layoutSidenav">
        <div id="layoutSidenav_nav">
          <nav className="sb-sidenav accordion sb-sidenav-dark" id="sidenavAccordion">
            <div className="sb-sidenav-menu">
              <div className="nav">
                <div className="sb-sidenav-menu-heading">Chức năng chính</div>
                <Link to="/" className="nav-link">
                  <div className="sb-nav-link-icon"><i className="fas fa-tachometer-alt"></i></div>
                  Tiếp đón
                </Link>
                
                <a className="nav-link collapsed" href="#" data-bs-toggle="collapse" data-bs-target="#collapseLayouts"
                  aria-expanded="false" aria-controls="collapseLayouts">
                  <div className="sb-nav-link-icon"><i className="fas fa-columns"></i></div>
                  Phòng khám
                  <div className="sb-sidenav-collapse-arrow"><i className="fas fa-angle-down"></i></div>
                </a>
                <div className="collapse" id="collapseLayouts" aria-labelledby="headingOne" data-bs-parent="#sidenavAccordion">
                  <nav className="sb-sidenav-menu-nested nav">
                    <Link className="nav-link" to="/encounter/pending">Danh sách chờ khám</Link>
                    <Link className="nav-link" to="/encounter/complete">Lịch sử khám bệnh</Link>
                  </nav>
                </div>

                <div className="sb-sidenav-menu-heading">Cài đặt</div>
                <a className="nav-link collapsed" href="#" data-bs-toggle="collapse" data-bs-target="#collapsePages"
                  aria-expanded="false" aria-controls="collapsePages">
                  <div className="sb-nav-link-icon"><i className="fas fa-book-open"></i></div>
                  Hệ thống
                  <div className="sb-sidenav-collapse-arrow"><i className="fas fa-angle-down"></i></div>
                </a>
                <div className="collapse" id="collapsePages" aria-labelledby="headingTwo" data-bs-parent="#sidenavAccordion">
                  <nav className="sb-sidenav-menu-nested nav accordion" id="sidenavAccordionPages">
                    <a className="nav-link collapsed" href="#" data-bs-toggle="collapse" data-bs-target="#pagesCollapseAuth"
                      aria-expanded="false" aria-controls="pagesCollapseAuth">
                      Tài khoản
                      <div className="sb-sidenav-collapse-arrow"><i className="fas fa-angle-down"></i></div>
                    </a>
                    <div className="collapse" id="pagesCollapseAuth" aria-labelledby="headingOne"
                      data-bs-parent="#sidenavAccordionPages">
                      <nav className="sb-sidenav-menu-nested nav">
                        <Link className="nav-link" to="/system/account/role">Vai trò</Link>
                        <Link className="nav-link" to="/system/account/user">Người sử dụng</Link>
                      </nav>
                    </div>
                  </nav>
                </div>
              </div>
            </div>
            <div className="sb-sidenav-footer">
              <div className="small">Đăng đăng nhập:</div>
              Admin
            </div>
          </nav>
        </div>
        <div id="layoutSidenav_content">
          <main>
            <Routes>
              <Route exact path="/" element={<Reception/>}/>
              <Route path="/encounter/pending" element={<PendingVisit/>}/>
              <Route path="/encounter/complete" element={<CompleteVisit/>}/>
              <Route path="/system/account/role" element={<RolePage/>}/>
              <Route path="/system/account/user" element={<UserPage/>}/>
            </Routes>
          </main>
          <footer className="py-4 bg-light mt-auto">
            <div className="container-fluid px-4">
              <div className="d-flex align-items-center justify-content-between small">
                <div className="text-muted">Bản quyền &copy; thuộc về ...</div>
                <div>
                  <a href="#">Chính sách riêng từ</a>
                  &middot;
                  <a href="#">Điều khoản sử dụng</a>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </>
  )
}