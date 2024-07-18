import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';

const ProfilePageContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: #001f3f;
    color: white;
`;

const ProfileCard = styled.div`
    background-color: #0074D9;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    text-align: center;
    width: 300px;
`;

const Title = styled.h1`
    color: #7FDBFF;
    margin-bottom: 20px;
`;

const Email = styled.p`
    font-size: 18px;
    color: #FFFFFF;
    margin: 10px 0;
`;

const Error = styled.div`
    color: #FF4136;
    background-color: #FFDC00;
    padding: 10px;
    border-radius: 5px;
    margin: 20px;
`;

const ProfilePage = () => {
    const [email, setEmail] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUserInfo = async () => {
            try {
                const response = await axios.get('http://localhost:8000/user-profile', { withCredentials: true });
                setEmail(response.data.email);
            } catch (error) {
                setError(error.response ? error.response.data.error : 'Error fetching user information');
            }
        };

        fetchUserInfo();
    }, []);

    if (error) {
        return <ProfilePageContainer><Error>{error}</Error></ProfilePageContainer>;
    }

    if (!email) {
        return <ProfilePageContainer><Email>Loading...</Email></ProfilePageContainer>;
    }

    return (
        <ProfilePageContainer>
            <ProfileCard>
                <Title>User Profile</Title>
                <Email>{email}</Email>
            </ProfileCard>
        </ProfilePageContainer>
    );
};

export default ProfilePage;