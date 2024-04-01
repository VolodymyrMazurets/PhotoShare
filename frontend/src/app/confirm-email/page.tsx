"use client";

import { Button, Col, Row, Typography, Spin } from "antd";
import axios from "@/api/axios";
import { useSearchParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { isNull } from "lodash";
import { Suspense } from "react";

const { Title } = Typography;

const ConfirmEmail: React.FC = () => {
  const params = useSearchParams();
  const router = useRouter();
  const [isSuccess, setIsSuccess] = useState<null | boolean>(null);

  const confirmEmail = useCallback(() => {
    const token = params.get("token");
    if (!token) {
      return setIsSuccess(false);
    }
    axios
      .get(`auth/confirmed_email/${token}`)
      .then(() => {
        setIsSuccess(true);
      })
      .catch(() => {
        if (isNull(isSuccess)) {
          setIsSuccess(false);
        }
      });
  }, [isSuccess, params]);

  const onButtonClick = useCallback(
    (type: "login" | "signup") => {
      if (type === "login") {
        router.push("/login");
      } else {
        router.push("/signup");
      }
    },
    [router]
  );

  useEffect(() => {
    confirmEmail();
  }, [confirmEmail]);

  return (
    <Suspense>
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
              <Title level={2} style={{ marginBottom: 24 }}>
                Email Confirmation
              </Title>

              <Row style={{ width: "100%" }}>
                {isNull(isSuccess) ? (
                  <Col span={24}>
                    <Spin tip="Loading" size="large">
                      <div className="content" style={{ height: 60 }} />
                    </Spin>
                  </Col>
                ) : (
                  <Col span={24}>
                    <Row>
                      {!isSuccess ? (
                        <Col span={24}>
                          <Title
                            level={4}
                            style={{
                              marginBottom: 32,
                              textAlign: "center",
                              color: "red",
                            }}
                          >
                            Invalid token
                          </Title>
                          <Button
                            type="primary"
                            style={{ width: "100%" }}
                            onClick={() => onButtonClick("signup")}
                          >
                            Sign up
                          </Button>
                        </Col>
                      ) : (
                        <Col span={24}>
                          <Title
                            level={4}
                            style={{
                              marginBottom: 32,
                              textAlign: "center",
                              color: "green",
                            }}
                          >
                            Email confirmed successfully
                          </Title>
                          <Button
                            type="primary"
                            style={{ width: "100%" }}
                            onClick={() => onButtonClick("login")}
                          >
                            Login
                          </Button>
                        </Col>
                      )}
                    </Row>
                  </Col>
                )}
              </Row>
            </div>
          </Col>
        </Row>
      </div>
    </Suspense>
  );
};

export default ConfirmEmail;
