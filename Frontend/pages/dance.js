import React from 'react';
import Layout from '../components/Layout';

const GifPage = () => {
return (
    <Layout>
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Enjoy the GIF!</h1>
            <img src="/pepe-dance-pepe-break.gif" alt="A cool GIF" style={{ maxWidth: '100%', height: 'auto' }} />
        </div>
    </Layout>
);
};

export default GifPage;