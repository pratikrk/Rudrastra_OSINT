// import logo from './logo.svg';
// import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Navbar, Footer } from "./containers";
import { Home, Signup, UserProfile, Login, About } from "./components";

function App() {
  return (
    <>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/user/profile" element={<UserProfile />} />
          <Route path="/user/signup" element={<Signup />} />
          <Route path="/user/login" element={<Login />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </>
  );
}

export default App;
