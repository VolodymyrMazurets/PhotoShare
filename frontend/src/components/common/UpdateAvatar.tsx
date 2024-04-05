"use client";

import { Button, Form, type FormProps, Upload, UploadFile } from "antd";
import axios from "@/api/axios";
import { toast } from "react-toastify";
import { useState } from "react";

type FieldType = {
  file: {
    file: UploadFile;
  };
};

export default function UpdateAvatar({
  onCancel,
  onSuccess,
}: {
  onCancel: () => void;
  onSuccess: () => void;
}) {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const onFinish: FormProps<FieldType>["onFinish"] = async (values) => {
    const data = new FormData();
    console.log(values.file);
    
    data.append("file", values.file?.file?.originFileObj || "");
    setLoading(true);
    axios
      .patch("avatar", data)
      .then(() => {
        toast.success("Avatar updated successfully");
        form.resetFields();
        onSuccess();
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <>
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
          label="New Avatar"
          name="file"
          rules={[{ required: true }]}
        >
          <Upload>
            <Button>Click to Upload</Button>
          </Upload>
        </Form.Item>

        <Form.Item wrapperCol={{ span: 24 }}>
          <Button
            loading={loading}
            style={{ width: "100%" }}
            type="primary"
            htmlType="submit"
          >
            Upload
          </Button>
        </Form.Item>
        <Button style={{ width: "100%" }} onClick={onCancel}>
          Cancel
        </Button>
      </Form>
    </>
  );
}
