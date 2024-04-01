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
import axios from "@/api/axios";
import { toast } from "react-toastify";

const { Title } = Typography;

type FieldType = {
  title?: string;
  description?: string;
  image?: {
    file: UploadFile;
  };
  tags?: string;
};

export default function CreatePost({
  onCancel,
  onSuccess,
}: {
  onCancel: () => void;
  onSuccess: () => void;
}) {
  const [form] = Form.useForm();

  const onFinish: FormProps<FieldType>["onFinish"] = async (values) => {
    const data = new FormData();
    data.append("tags", values.tags || "");
    data.append("image", values.image?.file?.originFileObj || "");
    axios
      .post("posts/", data, {
        params: {
          title: values.title,
          description: values.description,
        },
      })
      .then(() => {
        toast.success("Post created successfully");
        form.resetFields();
        onSuccess();
      });
  };

  return (
    <>
      <Title level={2}>Welcome to the app</Title>
      <Form
        name="basic"
        form={form}
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
          rules={[{ required: true, message: "Please input your password!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item<FieldType> label="Tags (comma separated)" name="tags">
          <Input />
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
          <Button style={{ width: "100%" }} type="primary" htmlType="submit">
            Create
          </Button>
        </Form.Item>
        <Button style={{ width: "100%" }} onClick={onCancel}>
          Cancel
        </Button>
      </Form>
    </>
  );
}
