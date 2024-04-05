/* eslint-disable @next/next/no-img-element */
"use client";

import { useCallback, useEffect, useState } from "react";
import axios from "@/api/axios";
import { PostType } from "@/components/pages/Home";
import { Avatar, Button, Col, Row } from "antd";
import { isNull, map } from "lodash";
import { UserOutlined, ArrowLeftOutlined } from "@ant-design/icons";
import { useRouter } from "next/navigation";
import BlockWrapper from "@/components/common/BlockWrapper";

export default function Post({ params }: { params: { id: number } }) {
  const [post, setPost] = useState<PostType | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const getAllPosts = useCallback(() => {
    setLoading(true);
    axios
      .get(`posts/${params.id}`)
      .then((res) => {
        setPost(res.data);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [params.id]);

  const onTransform = useCallback(() => {
    setLoading(true);
    axios
      .post(`posts/${params.id}/transform`, {}, {params: {
        gravity: "face",
        height: 200,
        width: 200,
        radius: "max",
      },})
      .then((res) => {
        if (!isNull(post)) {
          setPost({
            ...post,
            transformed_image: res.data.image,
          });
        }
      })
      .finally(() => {
        setLoading(false);
      });
  }, [params.id, post]);

  const onTransformQr = useCallback(() => {
    setLoading(true);
    axios
      .post(`posts/${params.id}/qr`)
      .then((res) => {
        if (!isNull(post)) {
          setPost({
            ...post,
            transformed_image_qr: res.data.image,
          });
        }
      })
      .finally(() => {
        setLoading(false);
      });
  }, [params.id, post]);

  useEffect(() => {
    getAllPosts();
  }, [getAllPosts]);

  if (!post) {
    return <h1>Loading ...</h1>
  }

  return (
    <div
      style={{
        width: "100%",
        maxWidth: 1000,
        margin: "auto",
        padding: 24,
        height: "100vh",
        overflow: "auto",
        background: "rgba(255, 255, 255, 0.3)",
        borderRadius: 12,
      }}
    >
      <Row gutter={32} align="stretch">
        <Col span={16}>
          <BlockWrapper>
            {post && (
              <Row gutter={[16, 16]} style={{ height: "100%" }}>
                <Col span={24}>
                  <Button
                    type="link"
                    onClick={() => router.push("/")}
                    icon={<ArrowLeftOutlined />}
                  >
                    Back
                  </Button>
                </Col>
                <Col span={24}>
                  <h1>{post.title}</h1>
                </Col>
                <Col span={24}>
                  <p>{post.description}</p>
                </Col>
                <Col span={24}>
                  <img
                    width="100%"
                    height="400px"
                    style={{
                      objectFit: "cover",
                      borderRadius: 12,
                    }}
                    alt={post.title}
                    src={post.image}
                  />
                </Col>
                <Col span={24}>
                  <Row gutter={[8, 8]}>
                    {map(post.tags, (tag) => (
                      <Col key={tag.id}>
                        <span
                          style={{
                            padding: 8,
                            background: "rgba(0, 0, 0, 0.1)",
                            borderRadius: 8,
                          }}
                        >
                          {tag.name}
                        </span>
                      </Col>
                    ))}
                  </Row>
                </Col>
                <Col span={24}>
                  <BlockWrapper>
                    <Row gutter={[8, 8]}>
                      {map(post.comments, (comment) => (
                        <Col span={24}>
                          <Row gutter={[10, 10]}>
                            <Col span={24}>
                              <Row align={"middle"} gutter={8}>
                                <Col>
                                  <Avatar
                                    size={16}
                                    icon={<UserOutlined />}
                                    src={comment.user?.avatar}
                                  />
                                </Col>
                                <Col>{comment.user.username}</Col>
                              </Row>
                            </Col>
                            <Col span={24}>{comment.content}</Col>
                          </Row>
                        </Col>
                      ))}
                    </Row>
                  </BlockWrapper>
                </Col>
              </Row>
            )}
          </BlockWrapper>
        </Col>
        <Col span={8}>
          <BlockWrapper style={{ height: "100%" }}>
            <Row gutter={[16, 16]}>
              <Col
                span={24}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                }}
              >
                <h3 style={{ marginBottom: 10 }}>Transformed image</h3>
                {post?.transformed_image ? (
                  <img
                    width="100px"
                    height="100px"
                    style={{
                      objectFit: "cover",
                      borderRadius: 12,
                      margin: "auto",
                    }}
                    alt={post?.title}
                    src={post?.transformed_image}
                  />
                ) : (
                  <Button loading={loading} onClick={onTransform}>
                    Transform post image
                  </Button>
                )}
              </Col>
              <Col
                span={24}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                }}
              >
                <h3 style={{ marginBottom: 10 }}>QR code</h3>
                {post?.transformed_image_qr ? (
                  <img
                    width="100%"
                    height="100%"
                    style={{
                      objectFit: "cover",
                      borderRadius: 12,
                      margin: "auto",
                    }}
                    alt="qr"
                    src={post?.transformed_image_qr}
                  />
                ) : (
                  <Button loading={loading} onClick={onTransformQr}>
                    Generate QR
                  </Button>
                )}
              </Col>
            </Row>
          </BlockWrapper>
        </Col>
      </Row>
    </div>
  );
}
