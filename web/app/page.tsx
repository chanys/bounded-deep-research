import { redirect } from "next/navigation";

// The app has no separate landing page; / sends you straight to the query UI.
export default function Home() {
  redirect("/query");
}
