/* eslint-disable @next/next/no-img-element */
import { useCallback, useEffect, useState } from "react";
import BlockWrapper from "../common/BlockWrapper";
import { toast } from "react-toastify";
import {
  Avatar,
  Col,
  Row,
  Typography,
  Card,
  Segmented,
  Button,
  Modal,
  Empty,
  Tag,
} from "antd";
import {
  UserOutlined,
  DeleteOutlined,
  EditOutlined,
  EllipsisOutlined,
  PlusOutlined,
} from "@ant-design/icons";
import { map, isEmpty } from "lodash";
import CreatePost from "../common/CreatePost";
import { deleteCookie } from "cookies-next";
import { useRouter } from "next/navigation";
import axios from "@/api/axios";

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
  const [currentView, setCurrentView] = useState<string>("All Posts");
  const [modalVisibility, setModalVisibility] = useState<boolean>(false);

  const router = useRouter();

  const getAllPosts = useCallback(() => {
    axios
      .get("posts", { params: { is_own: currentView !== "All Posts" } })
      .then((res) => {
        setPosts(res.data);
      });
  }, [currentView]);

  const getUserProfile = useCallback(() => {
    axios.get("profile/me").then((res) => {
      setUser(res.data);
    });
  }, []);

  const refetchData = useCallback(() => {
    getAllPosts();
  }, [getAllPosts]);

  const onDeletePost = useCallback(
    (postId: number) => {
      axios
        .delete(`http://localhost:8000/api/v1/posts/${postId}`)
        .then((res) => {
          toast.success(res.data.detail || "Success");
          refetchData();
        });
    },
    [refetchData]
  );

  const onAddNewPostClick = useCallback(() => {
    setModalVisibility(true);
  }, []);

  const onLogoutClick = () => {
    deleteCookie("token");
    deleteCookie("refresh_token");
    router.push("/login");
  };

  useEffect(() => {
    refetchData();
  }, [currentView, getAllPosts, refetchData]);

  useEffect(() => {
    getUserProfile();
  }, [getUserProfile]);

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
      <Modal
        title="Basic Modal"
        open={modalVisibility}
        onCancel={() => setModalVisibility(false)}
        footer={null}
      >
        <CreatePost
          onCancel={() => setModalVisibility(false)}
          onSuccess={() => {
            refetchData();
            setModalVisibility(false);
          }}
        />
      </Modal>
      <Row gutter={[32, 32]}>
        <Col span={24}>
          <BlockWrapper>
            <Row align="middle" justify="space-between" gutter={16}>
              <Col>
                <Row gutter={16} align="middle">
                  <Col>
                    <Avatar
                      size={48}
                      icon={<UserOutlined />}
                      src={user?.avatar}
                    />
                  </Col>
                  <Col>
                    <Title level={4} style={{ margin: 0 }}>
                      Welcome back <b>{user?.username}</b>! Your role is{" "}
                      <b>{user?.role}</b>
                    </Title>
                  </Col>
                </Row>
              </Col>
              <Col>
                <Button onClick={onLogoutClick}>Logout</Button>
              </Col>
            </Row>
          </BlockWrapper>
        </Col>
        <Col span={24}>
          <BlockWrapper>
            <Row gutter={[12, 12]}>
              <Col span={24}>
                <Row justify="space-between">
                  <Segmented<string>
                    options={["All Posts", "Own Post"]}
                    onChange={setCurrentView}
                  />
                  <Button icon={<PlusOutlined />} onClick={onAddNewPostClick}>
                    Add new post
                  </Button>
                </Row>
              </Col>
              {isEmpty(posts) ? (
                <Col
                  span={24}
                  style={{ display: "flex", justifyContent: "center" }}
                >
                  <Empty />
                </Col>
              ) : (
                map(posts, ({ id, image, title, description, user, tags }) => (
                  <Col span={6} key={id}>
                    <Card
                      hoverable
                      style={{
                        height: "100%",
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "space-between",
                      }}
                      cover={
                        <img
                          alt="example"
                          src={image}
                          style={{
                            width: "100%",
                            height: 250,
                            objectFit: "cover",
                          }}
                        />
                      }
                      actions={[
                        <DeleteOutlined
                          key="delete"
                          onClick={() => onDeletePost(id)}
                        />,
                        <EditOutlined key="edit" />,
                        <EllipsisOutlined key="ellipsis" />,
                      ]}
                    >
                      <Meta
                        style={{ flex: 1 }}
                        avatar={<Avatar src={user?.avatar} />}
                        title={
                          <Title level={5} style={{ margin: 0 }} ellipsis>
                            {title}
                          </Title>
                        }
                        description={
                          <Row>
                            <Col span={24}>
                              {map(tags, ({ id, name }) => (
                                <Tag key={id}>{name}</Tag>
                              ))}
                            </Col>
                            <Col span={24}>
                              <Text ellipsis>{description}</Text>
                            </Col>
                          </Row>
                        }
                      />
                    </Card>
                  </Col>
                ))
              )}
            </Row>
          </BlockWrapper>
        </Col>
      </Row>
    </div>
  );
}
