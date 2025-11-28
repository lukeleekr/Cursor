import Header from "@/components/header"
import Hero from "@/components/hero"
import Features from "@/components/features"
import Collections from "@/components/collections"
import About from "@/components/about"
import Contact from "@/components/contact"
import Footer from "@/components/footer"

export default function Home() {
  return (
    <main className="bg-background text-foreground">
      <Header />
      <Hero />
      <Features />
      <Collections />
      <About />
      <Contact />
      <Footer />
    </main>
  )
}
