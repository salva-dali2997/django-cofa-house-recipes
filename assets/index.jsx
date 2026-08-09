import { createRoot } from 'react-dom/client';
import App from './App.jsx';

const recipesData = JSON.parse(document.getElementById('recipes-data').textContent);

createRoot(document.getElementById('root')).render(<App recipes={recipesData} />);
