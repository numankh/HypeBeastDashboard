import {Navbar,
        Nav,
        NavDropdown,
        Container} from 'react-bootstrap';

export default function CustomNavbar() {
    return (
        <div>
            <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
                <Container>
                <Navbar.Brand href="/">HypeBeastHelper</Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                <Nav className="me-auto">
                    <Nav.Link href="trending">Trending Shoes</Nav.Link>
                    <Nav.Link href="sitecomp">Site Comparison</Nav.Link>
                    <NavDropdown title="Analytics" id="collasibles-nav-dropdown">
                        <NavDropdown.Item href="analytics/shoes/all">All Shoes</NavDropdown.Item>
                        <NavDropdown.Item href="analytics/shoes/notsold">Not Sold Shoes</NavDropdown.Item>
                        <NavDropdown.Item href="analytics/shoes/sold">Sold Shoes</NavDropdown.Item>
                    </NavDropdown>
                </Nav>
                </Navbar.Collapse>
                </Container>
            </Navbar>
        </div>
    );
}