import React, { useEffect } from 'react';

const Login = () => {
    useEffect(() => {
        window.location.href = 'http://localhost:8000/login';
    }, []);

    return (
        <div>
            <p>Redirecting to login...</p>
        </div>
    );
};

export default Login;