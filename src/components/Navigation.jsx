import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileProtectOutlined } from '@ant-design/icons';

const Navigation = () => {
  const navigate = useNavigate();

  const menuItems = [
    {
      key: 'policy',
      label: '政策申报',
      icon: <FileProtectOutlined />,
      onClick: () => navigate('/policy-application')
    },
  ];

  return (
    <div>
      {/* Render your menu items here */}
    </div>
  );
};

export default Navigation; 