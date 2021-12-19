import { render } from "react-dom";
import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import App from "./App";
import TrendingShoes from "./pages/trending";
import SiteComparison from "./pages/siteComp";
import AllShoes from "./pages/allShoes";
import NotSoldShoes from "./pages/listedShoes";
import SoldShoes from "./pages/soldShoes";

const rootElement = document.getElementById("root");
render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="trending" element={<TrendingShoes />} />
      <Route path="sitecomp" element={<SiteComparison />} />
      <Route path="analytics/shoes/all" element={<AllShoes />} />
      <Route path="analytics/shoes/notsold" element={<NotSoldShoes />} />
      <Route path="analytics/shoes/sold" element={<SoldShoes />} />
    </Routes>
  </BrowserRouter>,
  rootElement
);