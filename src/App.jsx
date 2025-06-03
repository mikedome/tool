import PolicyApplication from './pages/PolicyApplication';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/policy-application" element={<PolicyApplication />} />
      </Routes>
    </Router>
  );
}

export default App; 