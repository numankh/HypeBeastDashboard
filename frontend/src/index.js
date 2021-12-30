import { render } from "react-dom";
import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import App from "./App";
import TrendingShoes from "./pages/trending";
import SiteComparison from "./pages/siteComp";
import EbayShoeAnalytics from "./pages/ebayShoeAnalytics";

const rootElement = document.getElementById("root");
render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="trending" element={<TrendingShoes />} />
      <Route path="sitecomp" element={<SiteComparison />} />
      <Route path="analytics" element={<EbayShoeAnalytics />} />
    </Routes>
  </BrowserRouter>,
  rootElement
);