import type { Metadata } from "next";
import { AntdRegistry } from "@ant-design/nextjs-registry";
import { ConfigProvider } from "antd";
import Providers from "@/app/providers";
import "./globals.css";

export const metadata: Metadata = {
  title: "Photo Share App",
  description: "Awesome photo sharing app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <AntdRegistry>
            <ConfigProvider>{children}</ConfigProvider>
          </AntdRegistry>
        </Providers>
      </body>
    </html>
  );
}
