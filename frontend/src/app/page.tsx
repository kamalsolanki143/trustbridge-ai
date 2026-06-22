import Header from "@/components/Header"
import Navbar from "@/components/Navbar"
import Hero from "@/components/Hero"
import Features from "@/components/Features"
import WhyUs from "@/components/WhyUs"
import CTA from "@/components/CTA"
import FAQ from "@/components/FAQ"
import Footer from "@/components/Footer"

export default function Home() {
  return (
    <main>
      <Header />
      <Navbar />
      <Hero />
      <Features />
      <WhyUs />
      <CTA />
      <FAQ />
      <Footer />
    </main>
  )
}
