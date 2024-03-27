"use client";

import {
  Button,
  Form,
  type FormProps,
  Input,
  Col,
  Row,
  Typography,
} from "antd";
import axios from "axios";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";

type FieldType = {
  username?: string;
  password?: string;
  email?: string;
};

const { Title } = Typography;

const Signup: React.FC = () => {
  const router = useRouter();
  const [form] = Form.useForm();

  const onFinish: FormProps<FieldType>["onFinish"] = (values) => {
    axios
      .post("http://localhost:8000/api/auth/signup", values)
      .then((res) => {
        toast.success(res.data.detail);
        form.resetFields();
      })
      .catch((err) => {
        if (err.response?.data?.detail) {
          toast.error(err.response.data.detail);
        } else {
          toast.error('Something going wrong!');

        }
      });
  };

  const onFinishFailed: FormProps<FieldType>["onFinishFailed"] = (
    errorInfo
  ) => {
    console.log("Failed:", errorInfo);
  };

  const onLoginClick = () => {
    router.push("/login");
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
              backgroundColor: "white",
            }}
          >
            <Title level={2} style={{ marginBottom: 32 }}>
              Login to PhotoShare
            </Title>
            <Form
              name="signup"
              form={form}
              style={{ width: "100%" }}
              initialValues={{ remember: true }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              autoComplete="off"
              layout="vertical"
            >
              <Form.Item<FieldType>
                label="Username"
                name="username"
                rules={[
                  { required: true, message: "Please input your username!" },
                  {
                    min: 5,
                    message: "Username must be at least 5 characters!",
                  },
                ]}
              >
                <Input />
              </Form.Item>
              <Form.Item<FieldType>
                label="Email"
                name="email"
                rules={[
                  { required: true, message: "Please input your username!" },
                  { type: "email", message: "Please input a valid email!" },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item<FieldType>
                label="Password"
                name="password"
                rules={[
                  { required: true, message: "Please input your password!" },
                  {
                    min: 6,
                    message: "Password must be at least 6 characters!",
                  },
                ]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item wrapperCol={{ span: 24 }}>
                <Button
                  style={{ width: "100%" }}
                  type="primary"
                  htmlType="submit"
                >
                  Sign Up
                </Button>
              </Form.Item>
            </Form>
            <Button type="link" onClick={onLoginClick}>
              Log in to an existing account
            </Button>
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default Signup;
