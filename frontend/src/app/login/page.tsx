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
import { generateFormDataFromObject, parseJwt } from "@/utils";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";
import { setCookie } from "cookies-next";
import {fromUnixTime} from 'date-fns';

type FieldType = {
  username?: string;
  password?: string;
};

const { Title } = Typography;

const Login: React.FC = () => {
  const router = useRouter();

  const onFinish: FormProps<FieldType>["onFinish"] = async (values) => {
    const data = generateFormDataFromObject(values);
    axios
      .post("http://localhost:8000/api/v1/auth/login", data)
      .then((res) => {
        setCookie("token", res.data.access_token, {expires: fromUnixTime(parseJwt(res.data.access_token)?.exp)});
        setCookie("refresh_token", res.data.refresh_token);
        toast.success("Login successfully!");
        router.push("/");
      })
      .catch((err) => {
        toast.error(err.response.data.detail || "Something going wrong!");
      });
  };

  const onFinishFailed: FormProps<FieldType>["onFinishFailed"] = (
    errorInfo
  ) => {
    console.log("Failed:", errorInfo);
  };

  const onSignUpClick = () => {
    router.push("/signup");
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
              name="basic"
              style={{ width: "100%" }}
              initialValues={{ remember: true }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              autoComplete="off"
              layout="vertical"
            >
              <Form.Item<FieldType>
                label="Email"
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

              <Form.Item wrapperCol={{ span: 24 }}>
                <Button
                  style={{ width: "100%" }}
                  type="primary"
                  htmlType="submit"
                >
                  Login
                </Button>
              </Form.Item>
            </Form>
            <Button type="link" onClick={onSignUpClick}>
              Sign up fo an account
            </Button>
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default Login;
