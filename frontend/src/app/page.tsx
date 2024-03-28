"use client";

import {
  Button,
  Form,
  type FormProps,
  Input,
  Col,
  Row,
  Typography,
  Upload,
  UploadFile,
} from "antd";
import axios from "axios";
import { deleteCookie } from "cookies-next";
import { useRouter } from "next/navigation";
import { getCookie } from "cookies-next";
import { toast } from "react-toastify";

const { Title } = Typography;

type FieldType = {
  title?: string;
  description?: string;
  image?: {
    file: UploadFile;
  };
};

export default function Page() {
  const router = useRouter();

  const onLogoutClick = () => {
    deleteCookie("token");
    deleteCookie("refresh_token");
    router.push("/login");
  };

  const onFinish: FormProps<FieldType>["onFinish"] = async (values) => {
    const data = new FormData();
    console.log(values.image);

    data.append("tags", JSON.stringify(["test", "test1"] || []));
    data.append("image", values.image?.file?.originFileObj || "");
    axios
      .post("http://localhost:8000/api/v1/upload-post", data, {
        headers: {
          Authorization: `Bearer ${getCookie("token")}`,
        },
        params: {
          title: values.title,
          description: values.description,
        },
      })
      .then((res) => {
        console.log(res);

        toast.success("Post created successfully");
      })
      .catch((err) => {
        toast.error(err.response.data.detail || "Something going wrong!");
      });
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
            <Title level={2}>Welcome to the app</Title>
            <Form
              name="basic"
              style={{ width: "100%" }}
              initialValues={{ remember: true }}
              onFinish={onFinish}
              autoComplete="off"
              layout="vertical"
            >
              <Form.Item<FieldType>
                label="Title"
                name="title"
                rules={[{ required: true, message: "Please input title!" }]}
              >
                <Input />
              </Form.Item>

              <Form.Item<FieldType>
                label="Description"
                name="description"
                rules={[
                  { required: true, message: "Please input your password!" },
                ]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item<FieldType>
                label="Image"
                name="image"
                rules={[{ required: true }]}
              >
                <Upload>
                  <Button>Click to Upload</Button>
                </Upload>
              </Form.Item>

              <Form.Item wrapperCol={{ span: 24 }}>
                <Button
                  style={{ width: "100%" }}
                  type="primary"
                  htmlType="submit"
                >
                  Create
                </Button>
              </Form.Item>
              <Button style={{ width: "100%" }} onClick={onLogoutClick}>
                Logout
              </Button>
            </Form>
          </div>
        </Col>
      </Row>
    </div>
  );
  // Define other routes and logic
}
