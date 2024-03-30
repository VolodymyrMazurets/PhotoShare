/* eslint-disable @next/next/no-img-element */
import { useEffect, useState } from "react";
import BlockWrapper from "../common/BlockWrapper";
import axios from "axios";
import { getCookie } from "cookies-next";
import { toast } from "react-toastify";
import { Avatar, Col, Row, Typography, Card } from "antd";
import {
  UserOutlined,
  SettingOutlined,
  EditOutlined,
  EllipsisOutlined,
} from "@ant-design/icons";
import { map } from "lodash";

const { Text, Title } = Typography;
const { Meta } = Card;

interface UserType {
  id: number;
  username: string;
  email: string;
  created_at: string;
  avatar: string;
  role: string;
}

interface TagType {
  id: string;
  name: string;
}

interface CommentType {
  id: number;
  content: string;
  post_id: number;
  created_at: string;
  updated_at: string;
}

interface PostType {
  id: number;
  title: string;
  description: string;
  created_at: string;
  image: string;
  user: UserType;
  tags: TagType[];
  comments: CommentType[];
  transformed_image: string;
  transformed_image_qr: string;
}

export default function Home() {
  const [posts, setPosts] = useState<PostType[]>([]);
  const [user, setUser] = useState<UserType | null>(null);

  useEffect(() => {
    axios
      .get("http://localhost:8000/api/v1/posts/all", {
        headers: {
          Authorization: `Bearer ${getCookie("token")}`,
        },
      })
      .then((res) => {
        setPosts(res.data);
      })
      .catch((err) => {
        toast.error(err.response.data.detail || "Something going wrong!");
      });
    axios
      .get("http://localhost:8000/api/v1/profile/me", {
        headers: {
          Authorization: `Bearer ${getCookie("token")}`,
        },
      })
      .then((res) => {
        setUser(res.data);
      })
      .catch((err) => {
        toast.error(err.response.data.detail || "Something going wrong!");
      });
  }, []);
  return (
    <div
      style={{
        width: "100%",
        maxWidth: 1200,
        margin: "auto",
        padding: 24,
        height: "100vh",
        overflow: "auto",
        background: "rgba(255, 255, 255, 0.3)",
        borderRadius: 12,
      }}
    >
      <Row gutter={[32, 32]}>
        <Col span={24}>
          <BlockWrapper>
            <Row align="middle" gutter={16}>
              <Col>
                <Avatar size={48} icon={<UserOutlined />} src={user?.avatar} />
              </Col>
              <Col>
                <Title level={4} style={{ margin: 0 }}>
                  Welcome back {user?.username}!
                </Title>
              </Col>
            </Row>
          </BlockWrapper>
        </Col>
        <Col span={24}>
          <BlockWrapper>
            <Row gutter={[12, 12]}>
              {map(posts, ({ id, image, title, description }) => (
                <Col span={6} key={id}>
                  <Card
                    hoverable
                    style={{ height: 400 }}
                    cover={
                      <img
                        alt="example"
                        src={image}
                        style={{
                          width: "100%",
                          height: 260,
                          objectFit: "cover",
                        }}
                      />
                    }
                    actions={[
                      <SettingOutlined key="setting" />,
                      <EditOutlined key="edit" />,
                      <EllipsisOutlined key="ellipsis" />,
                    ]}
                  >
                    <Meta
                      title={
                        <Title level={5} style={{ margin: 0 }} ellipsis>
                          {title}
                        </Title>
                      }
                      description={<Text ellipsis>{description}</Text>}
                    />
                  </Card>
                </Col>
              ))}
            </Row>
          </BlockWrapper>
        </Col>
      </Row>
    </div>
  );
}
