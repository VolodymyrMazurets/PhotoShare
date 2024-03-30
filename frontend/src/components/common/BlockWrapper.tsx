export default function BlockWrapper({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        background: "rgba(255, 255, 255, 0.7)",
        borderRadius: 12,
        padding: 24,
      }}
    >
      {children}
    </div>
  );
}
