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
import { useRouter } from "next/navigation";
import Home from "@/components/pages/Home";

const { Title } = Typography;

export default function Page() {
  const router = useRouter();

  return <Home />;
}
