# LLM Output

### Emergency Migration Assistant Platform

The following codebase implements the Emergency Migration Assistant platform as described in the task. This platform allows users to register using Aadhaar-based OTP verification, upload documents, and request emergency government services remotely.

#### src/App.jsx
```jsx
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { HashRouter, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { clsx } from 'clsx';
import { Lucide } from 'lucide-react';
import { format } from 'date-fns';

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [aadhaarNumber, setAadhaarNumber] = useState('');
  const [otp, setOtp] = useState('');
  const [verified, setVerified] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [processedResult, setProcessedResult] = useState(null);
  const [serviceName, setServiceName] = useState('');
  const [serviceDescription, setServiceDescription] = useState('');
  const fileInputRef = useRef(null);

  const handleAadhaarChange = useCallback((e) => {
    setAadhaarNumber(e.target.value);
  }, []);

  const handleOtpChange = useCallback((e) => {
    setOtp(e.target.value);
  }, []);

  const handleVerify = useCallback(async () => {
    try {
      const response = await axios.post(`${BASE_URL}/api/v1/verify`, {
        aadhaarNumber,
        otp,
      });
      if (response.data.success) {
        setVerified(true);
        toast.success('Verified successfully!');
      } else {
        toast.error('Verification failed!');
      }
    } catch (error) {
      toast.error('Error occurred during verification!');
    }
  }, [aadhaarNumber, otp]);

  const handleFileChange = useCallback((e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  }, []);

  const handleProcess = useCallback(async () => {
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      const response = await axios.post(`${BASE_URL}/api/v1/process`, formData);
      setProcessedResult(response.data);
    } catch (error) {
      toast.error('Error occurred during processing!');
    }
  }, [selectedFile]);

  const handleServiceRequest = useCallback(async () => {
    try {
      const response = await axios.post(`${BASE_URL}/api/v1/request-service`, {
        serviceName,
        serviceDescription,
      });
      if (response.data.success) {
        toast.success('Service requested successfully!');
      } else {
        toast.error('Service request failed!');
      }
    } catch (error) {
      toast.error('Error occurred during service request!');
    }
  }, [serviceName, serviceDescription]);

  useEffect(() => {
    if (verified) {
      axios.get(`${BASE_URL}/api/v1/documents`)
        .then((response) => {
          setDocuments(response.data);
        })
        .catch((error) => {
          toast.error('Error occurred while fetching documents!');
        });
    }
  }, [verified]);

  return (
    <HashRouter>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <h1 className="text-3xl font-bold mb-4">Emergency Migration Assistant</h1>
              <div className="flex flex-col items-center">
                <input
                  type="text"
                  value={aadhaarNumber}
                  onChange={handleAadhaarChange}
                  placeholder="Aadhaar Number"
                  className="w-full p-2 mb-2 border border-gray-400 rounded"
                />
                <input
                  type="text"
                  value={otp}
                  onChange={handleOtpChange}
                  placeholder="OTP"
                  className="w-full p-2 mb-2 border border-gray-400 rounded"
                />
                <button
                  onClick={handleVerify}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                  Verify
                </button>
              </div>
              {verified && (
                <div className="flex flex-col items-center mt-4">
                  <h2 className="text-2xl font-bold mb-2">Upload Documents</h2>
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    className="w-full p-2 mb-2 border border-gray-400 rounded"
                  />
                  <button
                    onClick={handleProcess}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  >
                    Process
                  </button>
                  {selectedFile && (
                    <div className="flex flex-col items-center mt-2">
                      <h3 className="text-xl font-bold mb-1">Original</h3>
                      <img src={URL.createObjectURL(selectedFile)} alt="Original" className="w-full h-64 object-cover" />
                      <p className="text-sm">{selectedFile.name} ({selectedFile.size} bytes)</p>
                    </div>
                  )}
                  {processedResult && (
                    <div className="flex flex-col items-center mt-2">
                      <h3 className="text-xl font-bold mb-1">Processed</h3>
                      <img src={processedResult} alt="Processed" className="w-full h-64 object-cover" />
                      <button
                        onClick={() => {
                          const link = document.createElement('a');
                          link.href = processedResult;
                          link.download = 'processed_image.jpg';
                          link.click();
                        }}
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                      >
                        Download
                      </button>
                    </div>
                  )}
                </div>
              )}
              {verified && (
                <div className="flex flex-col items-center mt-4">
                  <h2 className="text-2xl font-bold mb-2">Request Service</h2>
                  <input
                    type="text"
                    value={serviceName}
                    onChange={(e) => setServiceName(e.target.value)}
                    placeholder="Service Name"
                    className="w-full p-2 mb-2 border border-gray-400 rounded"
                  />
                  <textarea
                    value={serviceDescription}
                    onChange={(e) => setServiceDescription(e.target.value)}
                    placeholder="Service Description"
                    className="w-full p-2 mb-2 border border-gray-400 rounded"
                  />
                  <button
                    onClick={handleServiceRequest}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  >
                    Request Service
                  </button>
                </div>
              )}
            </>
          }
        />
      </Routes>
      <ToastContainer />
    </HashRouter>
  );
}

export default App;
```

#### src/main.jsx
```jsx
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
```

#### src/index.css
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-gray-100;
}

h1, h2, h3, p {
  @apply text-gray-600;
}

button {
  @apply rounded;
}

input, textarea {
  @apply border border-gray-400 rounded;
}
```

#### src/api.js
```javascript
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
});

export const verifyAadhaar = async (aadhaarNumber, otp) => {
  try {
    const response = await api.post('/api/v1/verify', {
      aadhaarNumber,
      otp,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const uploadDocument = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/v1/process', formData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const requestService = async (serviceName, serviceDescription) => {
  try {
    const response = await api.post('/api/v1/request-service', {
      serviceName,
      serviceDescription,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};
```

This implementation provides a basic structure for the Emergency Migration Assistant platform. It includes Aadhaar-based OTP verification, document upload, and service request features. The platform uses Tailwind CSS for styling and React Toastify for displaying notifications. The API requests are handled using Axios. The platform is designed to be user-friendly and accessible.

Note: This implementation is a starting point and may require additional features, error handling, and security measures to make it production-ready.