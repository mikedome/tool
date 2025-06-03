import React from 'react';
import { Card, Button, Row, Col } from 'antd';
import { useNavigate } from 'react-router-dom';

const PolicyApplication = () => {
  const navigate = useNavigate();

  const policyTypes = [
    {
      title: '科技型中小企业',
      description: '面向科技创新能力突出的中小企业的扶持政策',
    },
    {
      title: '创新型中小企业',
      description: '支持具有自主创新能力和发展潜力的中小企业',
    },
    {
      title: '专精特新中小企业',
      description: '针对专业化、精细化、特色化、新颖化中小企业的支持政策',
    },
    {
      title: '高新技术企业',
      description: '高新技术企业认定及相关优惠政策',
    }
  ];

  return (
    <div className="policy-application" style={{ padding: '24px' }}>
      <h2>政策申报</h2>
      <Row gutter={[16, 16]}>
        {policyTypes.map((policy, index) => (
          <Col xs={24} sm={12} md={8} lg={6} key={index}>
            <Card
              hoverable
              style={{ height: '100%' }}
              onClick={() => navigate(`/policy-detail/${index}`)}
            >
              <h3>{policy.title}</h3>
              <p>{policy.description}</p>
              <Button type="primary">查看详情</Button>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default PolicyApplication; 