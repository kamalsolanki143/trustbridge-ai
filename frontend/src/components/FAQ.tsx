"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

const faqs = [
  {
    q: "How does TrustBridge access my financial data?",
    a: "Through RBI's Account Aggregator framework — a consent-based system where you approve exactly what data is shared, with whom, and for how long. No passwords. No manual uploads. Revoke anytime.",
  },
  {
    q: "What if my business doesn't have GST registration?",
    a: "TrustBridge uses a tiered data model. Even with only UPI transaction history, you receive a Starter Score. As you connect more data sources, your coverage improves and your grade updates in real time.",
  },
  {
    q: "How is this different from a CIBIL score?",
    a: "CIBIL measures past credit behavior. TrustBridge measures current financial health — cash flows, compliance activity, and growth signals — for businesses that may have never borrowed before.",
  },
  {
    q: "What does 'Improve First' outcome mean?",
    a: "It means your business isn't ready today, but we show you exactly why and what to fix. Connect GST data, extend your transaction history by 3 months, reduce bounced payments — and your grade improves automatically.",
  },
  {
    q: "How accurate is the 10-second assessment?",
    a: "The system uses a multi-factor weighted scoring model across cash flow, compliance, repayment capacity, and growth signals. Confidence bands are shown with every grade so lenders always know how much data backs the decision.",
  },
  {
    q: "Is my data stored after the assessment?",
    a: "Assessment results are stored for audit purposes with your consent. Raw financial data is never stored — it is fetched, analysed, and discarded per AA framework guidelines.",
  },
  {
    q: "Can a bank officer override the AI decision?",
    a: "Yes. The Manual Review stage exists exactly for this. TrustBridge supports decisions, it does not replace human judgment. Every output includes full reason codes for the officer to review.",
  },
  {
    q: "What loan types can this assess eligibility for?",
    a: "Working Capital Loans, Term Loans, Invoice Financing, and MUDRA-linked products. The Credit Ladder Engine maps readiness grades to appropriate product recommendations.",
  },
]

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null)

  return (
    <section id="faq" className="px-6 py-24 md:py-32" style={{ backgroundColor: "#07080F" }}>
      <div className="mx-auto max-w-3xl">
        <div className="mb-16 text-center">
          <p className="mb-4 font-mono text-[11px] font-medium tracking-[0.2em]" style={{ color: "#00C9A7" }}>
            COMMON QUESTIONS
          </p>
          <h2 className="text-[36px] font-semibold leading-tight tracking-[-1px] md:text-[42px]" style={{ fontFamily: "'Space Grotesk', sans-serif", color: "#F0F2FF" }}>
            Everything you need to know.
          </h2>
        </div>

        <div>
          {faqs.map((faq, i) => {
            const isOpen = openIndex === i
            return (
              <div
                key={i}
                className="border-b transition-all duration-200"
                style={{
                  borderColor: "#1C1D2E",
                  borderLeft: isOpen ? "3px solid #00C9A7" : "3px solid transparent",
                }}
              >
                <button
                  onClick={() => setOpenIndex(isOpen ? null : i)}
                  className="flex w-full items-center justify-between px-5 py-5 text-left text-base font-medium transition-colors md:px-6"
                  style={{
                    color: "#F0F2FF",
                    fontFamily: "'Inter', sans-serif",
                    fontWeight: 500,
                  }}
                >
                  <span>{faq.q}</span>
                  <span
                    className="ml-4 flex h-6 w-6 shrink-0 items-center justify-center text-sm font-bold transition-transform duration-200"
                    style={{
                      color: "#00C9A7",
                      transform: isOpen ? "rotate(45deg)" : "rotate(0deg)",
                    }}
                  >
                    +
                  </span>
                </button>
                <AnimatePresence>
                  {isOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3, ease: "easeInOut" as const }}
                      className="overflow-hidden"
                    >
                      <p
                        className="px-5 pb-6 text-[15px] leading-relaxed md:px-6"
                        style={{
                          color: "#8B8FA8",
                          fontFamily: "'Inter', sans-serif",
                          lineHeight: 1.7,
                        }}
                      >
                        {faq.a}
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
