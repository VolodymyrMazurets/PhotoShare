"use client";

import {
  Button,
  Form,
  type FormProps,
  Input,
  Col,
  Row,
  Typography,
  notification,
} from "antd";
import axios from "axios";

type FieldType = {
  username?: string;
  password?: string;
};

const { Title } = Typography;

const Login: React.FC = () => {
  const onFinish: FormProps<FieldType>["onFinish"] = (values) => {
    const formData = new FormData();
    formData.append("username", values.username || "");
    formData.append("password", values.password || "");
    axios
      .post("http://localhost:8000/api/auth/login", formData)

      .then((res) => {
        console.log(res);
        notification.info({
          message: `Success!`,
          description: (
              <code>{JSON.stringify(res.data)}</code>
          ),
          placement: "topRight",
        });
      })
      .catch((err) => {
        notification.error({
          message: `Error!`,
          description: err.response.data.detail,
          placement: "topRight",
        });
      });
  };

  const onFinishFailed: FormProps<FieldType>["onFinishFailed"] = (
    errorInfo
  ) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <div style={{ height: "100vh", width: "100%", overflow: "hidden" }}>
      <Row
        justify="center"
        align="middle"
        style={{ height: "100%", width: "100%" }}
      >
        <Col span="12" style={{ maxWidth: 420 }}>
          <div
            style={{
              padding: 32,
              boxShadow: "rgba(100, 100, 111, 0.2) 0px 7px 29px 0px",
              maxWidth: 420,
              display: "flex",
              justifyContent: "center",
              flexDirection: "column",
              alignItems: "center",
              borderRadius: 12,
            }}
          >
            <Title level={2} style={{ marginBottom: 48 }}>
              Login to PhotoShare
            </Title>
            <Form
              name="basic"
              style={{ width: "100%" }}
              initialValues={{ remember: true }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              autoComplete="off"
            >
              <Form.Item<FieldType>
                label="Username"
                name="username"
                rules={[
                  { required: true, message: "Please input your username!" },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item<FieldType>
                label="Password"
                name="password"
                rules={[
                  { required: true, message: "Please input your password!" },
                ]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item wrapperCol={{ span: 24 }} noStyle>
                <Button
                  style={{ width: "100%" }}
                  type="primary"
                  htmlType="submit"
                >
                  Submit
                </Button>
              </Form.Item>
            </Form>
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default Login;
