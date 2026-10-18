/**
 * AI E-Commerce Management System (Amazon India) - SPA Application Controller
 * Handles live data loading, 12-agent pipeline dispatches, approval workflows,
 * interactive fee calculations, and emergency stop controls.
 */

// Global State
const state = {
  currentSection: "business-overview",
  products: [],
  selectedForCompare: new Set(),
  emergencyStopActive: false,
  pendingApprovalsCount: 0
};

// Formatting Helpers
function formatINR(amount) {
  if (amount === undefined || amount === null || isNaN(amount)) return "₹0.00";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2
  }).format(amount);
}

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  if (!container) return;
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<strong>${type.toUpperCase()}:</strong> ${message}`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

// Navigation Handler
function navigateToSection(sectionId) {
  state.currentSection = sectionId;
  document.querySelectorAll(".nav-item").forEach(item => {
    item.classList.toggle("active", item.getAttribute("data-section") === sectionId);
  });
  document.querySelectorAll(".section-view").forEach(view => {
    view.classList.toggle("active", view.id === `section-${sectionId}`);
  });

  // Load section-specific data
  if (sectionId === "business-overview") loadOverviewData();
  else if (sectionId === "product-research") loadProductsTable();
  else if (sectionId === "approval-centre") loadApprovals();
  else if (sectionId === "inventory-management") loadInventory();
  else if (sectionId === "listing-drafts") loadListings();
  else if (sectionId === "daily-reports") loadDailyReports();
  else if (sectionId === "integration-settings") loadIntegrations();
  else if (sectionId === "audit-logs") loadAuditLogs();
  else if (sectionId === "pricing-recommendations") loadPricing();
}

// 1. Business Overview Loader
async function loadOverviewData() {
  try {
    const [prodRes, appRes, invRes, repRes, estopRes] = await Promise.all([
      fetch("/api/products"),
      fetch("/api/approvals?status=PENDING"),
      fetch("/api/inventory"),
      fetch("/api/reports/latest"),
      fetch("/api/approvals/emergency-stop/status")
    ]);

    const products = await prodRes.json();
    const approvals = await appRes.json();
    const inventory = await invRes.json();
    const latestReport = await repRes.json();
    const estop = await estopRes.json();

    state.products = products;
    state.pendingApprovalsCount = approvals.length;
    state.emergencyStopActive = estop.emergency_stop_active;

    // Update Navigation Badge
    const badge = document.getElementById("nav-approval-badge");
    if (badge) {
      badge.textContent = approvals.length;
      badge.style.display = approvals.length > 0 ? "inline-block" : "none";
    }

    // Update Emergency Stop Button UI
    updateEmergencyStopUI(estop.emergency_stop_active);

    // KPI Values
    document.getElementById("kpi-total-products").textContent = products.length;
    document.getElementById("kpi-pending-approvals").textContent = approvals.length;

    const lowStock = inventory.filter(i => i.needs_reorder).length;
    document.getElementById("kpi-low-stock").textContent = lowStock;

    // Average Margin of approved/evaluated candidates
    const validMargins = products.filter(p => p.net_margin_pct > 0).map(p => p.net_margin_pct);
    const avgMargin = validMargins.length > 0 ? (validMargins.reduce((a, b) => a + b, 0) / validMargins.length).toFixed(1) : "0.0";
    document.getElementById("kpi-avg-margin").textContent = `${avgMargin}%`;

    // Render Briefing Summary
    const briefingEl = document.getElementById("overview-briefing-text");
    if (briefingEl && latestReport.summary) {
      briefingEl.textContent = latestReport.summary;
    }

    // Render Top Candidates Table
    const topTbody = document.getElementById("overview-top-candidates-tbody");
    if (topTbody) {
      topTbody.innerHTML = "";
      const topFive = [...products].sort((a, b) => b.overall_score - a.overall_score).slice(0, 5);
      topFive.forEach(p => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${p.title.substring(0, 45)}...</strong></td>
          <td>${p.category}</td>
          <td>${formatINR(p.selling_price_inr)}</td>
          <td><span class="badge ${p.net_margin_pct >= 15 ? 'badge-success' : 'badge-warning'}">${p.net_margin_pct}%</span></td>
          <td><strong>${p.overall_score}/100</strong></td>
          <td><span class="badge badge-${getStatusColor(p.status)}">${p.status}</span></td>
          <td><button class="btn btn-sm btn-secondary" onclick="viewProductDetail(${p.id})">Inspect</button></td>
        `;
        topTbody.appendChild(tr);
      });
    }
  } catch (err) {
    console.error("Error loading overview:", err);
  }
}

function getStatusColor(status) {
  switch (status) {
    case "APPROVED":
    case "ACTION_EXECUTED": return "success";
    case "AWAITING_APPROVAL": return "warning";
    case "REJECTED": return "danger";
    case "ANALYSED":
    case "RISK_CHECKED": return "info";
    default: return "secondary";
  }
}

// 2. Product Research Section
async function loadProductsTable() {
  const searchInput = document.getElementById("product-search-input")?.value || "";
  const categoryFilter = document.getElementById("product-category-filter")?.value || "";
  const statusFilter = document.getElementById("product-status-filter")?.value || "";

  let url = `/api/products?search=${encodeURIComponent(searchInput)}`;
  if (categoryFilter) url += `&category=${encodeURIComponent(categoryFilter)}`;
  if (statusFilter) url += `&status=${encodeURIComponent(statusFilter)}`;

  try {
    const res = await fetch(url);
    const products = await res.json();
    state.products = products;

    const tbody = document.getElementById("products-table-tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (products.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 2rem; color: var(--text-muted);">No products found matching filters.</td></tr>`;
      return;
    }

    products.forEach(p => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><input type="checkbox" onchange="toggleCompareProduct(${p.id}, this.checked)" ${state.selectedForCompare.has(p.id) ? 'checked' : ''}></td>
        <td>
          <div style="font-weight: 600;">${p.title}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">ASIN: ${p.asin || 'N/A'} | SKU: ${p.sku || 'N/A'}</div>
        </td>
        <td>${p.category}</td>
        <td>${formatINR(p.selling_price_inr)}</td>
        <td><span class="badge ${p.net_margin_pct >= 15 ? 'badge-success' : 'badge-danger'}">${p.net_margin_pct}%</span></td>
        <td>
          <div style="font-weight: 700;">${p.overall_score}/100</div>
          <div style="font-size: 0.7rem; color: ${p.gate_passed ? 'var(--accent-success)' : 'var(--accent-danger)'};">
            ${p.gate_passed ? '✓ Gates Passed' : '✗ Gate Rejected'}
          </div>
        </td>
        <td><span class="badge badge-${getStatusColor(p.status)}">${p.status}</span></td>
        <td>
          <div style="display: flex; gap: 0.35rem;">
            <button class="btn btn-sm btn-primary" onclick="triggerEvaluatePipeline(${p.id})">Run AI Agents</button>
            <button class="btn btn-sm btn-secondary" onclick="viewProductDetail(${p.id})">Details</button>
          </div>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    showToast("Failed to load products: " + err.message, "danger");
  }
}

// Trigger 12-Agent Pipeline
async function triggerEvaluatePipeline(productId) {
  showToast(`Running 12-agent pipeline for Product #${productId}...`, "info");
  try {
    const res = await fetch(`/api/products/${productId}/evaluate`, { method: "POST" });
    const data = await res.json();
    if (res.ok) {
      showToast(`Pipeline complete: Status is ${data.pipeline_status} (Score: ${data.overall_score || 0})`, "success");
      loadProductsTable();
      loadOverviewData();
    } else {
      showToast(`Pipeline failed: ${data.detail || 'Unknown error'}`, "danger");
    }
  } catch (err) {
    showToast("Pipeline network error: " + err.message, "danger");
  }
}

// Product Details Modal
async function viewProductDetail(productId) {
  try {
    const res = await fetch(`/api/products/${productId}`);
    const p = await res.json();

    const modal = document.getElementById("product-detail-modal");
    const content = document.getElementById("product-detail-modal-content");
    if (!modal || !content) return;

    let obsHtml = "<p>No market observation</p>";
    if (p.observation) {
      obsHtml = `
        <div style="background: rgba(15,23,42,0.8); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
          <div style="display:flex; justify-content:space-between; margin-bottom: 0.5rem;">
            <span class="provenance-tag">Source: ${p.observation.source}</span>
            <span class="provenance-tag">Data Type: ${p.observation.data_type}</span>
            <span class="provenance-tag">Confidence: ${p.observation.confidence}</span>
          </div>
          <div>Observed Price: <strong>${formatINR(p.observation.selling_price_inr)}</strong> (MRP: ${formatINR(p.observation.mrp_inr)})</div>
          <div>BSR Rank: <strong>#${p.observation.bsr_rank || 'N/A'}</strong> | Estimated Sales: <strong>${p.observation.estimated_monthly_sales || 0} units/month</strong></div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${p.observation.sales_method || ''}</div>
          <div>Reviews: <strong>${p.observation.review_count}</strong> | Rating: <strong>⭐ ${p.observation.rating_avg}</strong> | Competing Sellers: <strong>${p.observation.num_sellers}</strong></div>
        </div>
      `;
    }

    let profHtml = "<p>No profitability calculation</p>";
    if (p.profitability) {
      profHtml = `
        <div style="background: rgba(15,23,42,0.8); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
          <div>Target Selling Price: <strong>${formatINR(p.profitability.target_price)}</strong></div>
          <div>Supplier Base Cost: <strong>${formatINR(p.profitability.supplier_cost)}</strong></div>
          <div>Amazon Fees (Referral + Closing + Shipping): <strong>${formatINR(p.profitability.referral_fee + p.profitability.closing_fee + p.profitability.weight_fee)}</strong></div>
          <div>Amazon 18% GST: <strong>${formatINR(p.profitability.amazon_gst)}</strong></div>
          <div style="margin-top: 0.5rem; font-size: 1.1rem; color: var(--accent-success);">Net Operating Profit: <strong>${formatINR(p.profitability.net_profit)} (${p.profitability.net_margin_pct}%)</strong></div>
          <div>Return on Capital (ROI): <strong>${p.profitability.roi_pct}%</strong> | Break-even Price: <strong>${formatINR(p.profitability.breakeven_price)}</strong></div>
          <div>Max Affordable Ad Cost: <strong>${formatINR(p.profitability.max_ad_cost)}</strong></div>
        </div>
      `;
    }

    content.innerHTML = `
      <h3>${p.title}</h3>
      <div style="color: var(--text-secondary); margin-bottom: 1rem;">Category: ${p.category} | Weight: ${p.weight_grams}g | Channel: ${p.fulfilment_channel}</div>
      <div style="margin-bottom: 1rem;">
        <span class="badge badge-${getStatusColor(p.status)}">${p.status}</span>
        ${p.rejection_reason ? `<div style="color: var(--accent-danger); margin-top: 0.5rem;"><strong>Rejection Reason:</strong> ${p.rejection_reason}</div>` : ''}
      </div>
      <h4>Market & Sales Evidence</h4>
      ${obsHtml}
      <h4>Deterministic Unit Economics</h4>
      ${profHtml}
    `;

    modal.classList.add("active");
  } catch (err) {
    showToast("Error loading details: " + err.message, "danger");
  }
}

// 3. Product Comparison
function toggleCompareProduct(id, checked) {
  if (checked) state.selectedForCompare.add(id);
  else state.selectedForCompare.delete(id);

  const compareBtn = document.getElementById("btn-go-compare");
  if (compareBtn) {
    compareBtn.textContent = `Compare Selected (${state.selectedForCompare.size})`;
    compareBtn.style.display = state.selectedForCompare.size >= 2 ? "inline-flex" : "none";
  }
}

async function runComparisonView() {
  if (state.selectedForCompare.size < 2) {
    showToast("Select at least 2 products to compare", "warning");
    return;
  }
  const idStr = Array.from(state.selectedForCompare).join(",");
  try {
    const res = await fetch(`/api/products/compare/batch?ids=${idStr}`);
    const data = await res.json();

    const thead = document.getElementById("compare-table-thead");
    const tbody = document.getElementById("compare-table-tbody");
    if (!thead || !tbody) return;

    thead.innerHTML = `<tr><th>Metric</th>${data.map(p => `<th>${p.title.substring(0, 35)}...</th>`).join('')}</tr>`;

    const metrics = [
      { label: "Overall Score", key: "overall_score", format: v => `<strong>${v}/100</strong>` },
      { label: "Gate Status", key: "gate_passed", format: v => v ? '<span style="color:var(--accent-success)">PASSED</span>' : '<span style="color:var(--accent-danger)">FAILED</span>' },
      { label: "Category", key: "category", format: v => v },
      { label: "Selling Price", key: "selling_price", format: formatINR },
      { label: "Supplier Cost", key: "supplier_cost", format: formatINR },
      { label: "Net Margin %", key: "net_margin_pct", format: v => `<strong>${v}%</strong>` },
      { label: "Net Unit Profit", key: "net_profit_inr", format: formatINR },
      { label: "Return on Capital (ROI)", key: "roi_pct", format: v => `${v}%` },
      { label: "Est. Monthly Sales", key: "estimated_monthly_sales", format: v => `${v} units` },
      { label: "Review Count", key: "review_count", format: v => v },
      { label: "Customer Rating", key: "rating", format: v => `⭐ ${v}` }
    ];

    tbody.innerHTML = metrics.map(m => `
      <tr>
        <td><strong>${m.label}</strong></td>
        ${data.map(p => `<td>${m.format(p[m.key])}</td>`).join('')}
      </tr>
    `).join('');

    navigateToSection("product-comparison");
  } catch (err) {
    showToast("Comparison error: " + err.message, "danger");
  }
}

// 4. Interactive Profitability Calculator
async function recalculateLiveCalculator() {
  const category = document.getElementById("calc-category")?.value || "Home & Kitchen";
  const selling_price = parseFloat(document.getElementById("calc-selling-price")?.value || 0);
  const supplier_cost = parseFloat(document.getElementById("calc-supplier-cost")?.value || 0);
  const package_weight_grams = parseFloat(document.getElementById("calc-weight")?.value || 350);
  const fulfilment_channel = document.getElementById("calc-channel")?.value || "EASY_SHIP";
  const shipping_zone = document.getElementById("calc-zone")?.value || "NATIONAL";
  const inbound_shipping_per_unit = parseFloat(document.getElementById("calc-inbound")?.value || 20);
  const packaging_labelling_cost = parseFloat(document.getElementById("calc-packaging")?.value || 15);
  const estimated_ad_cost_per_unit = parseFloat(document.getElementById("calc-ad-cost")?.value || 40);

  try {
    const res = await fetch("/api/calculator", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        category,
        selling_price,
        supplier_cost,
        package_weight_grams,
        fulfilment_channel,
        shipping_zone,
        inbound_shipping_per_unit,
        packaging_labelling_cost,
        estimated_ad_cost_per_unit
      })
    });
    const c = await res.json();

    document.getElementById("calc-out-referral").textContent = formatINR(c.referral_fee);
    document.getElementById("calc-out-closing").textContent = formatINR(c.closing_fee);
    document.getElementById("calc-out-weight").textContent = formatINR(c.weight_handling_fee);
    document.getElementById("calc-out-amazon-gst").textContent = formatINR(c.amazon_fee_gst);
    document.getElementById("calc-out-net-gst").textContent = formatINR(c.net_gst_payable);
    document.getElementById("calc-out-contribution").textContent = formatINR(c.contribution_per_unit);
    document.getElementById("calc-out-net-profit").textContent = formatINR(c.net_operating_profit);
    document.getElementById("calc-out-net-margin").textContent = `${c.net_profit_margin_pct}%`;
    document.getElementById("calc-out-roi").textContent = `${c.roi_pct}%`;
    document.getElementById("calc-out-breakeven").textContent = formatINR(c.breakeven_selling_price);
    document.getElementById("calc-out-max-ad").textContent = formatINR(c.max_affordable_ad_cost);

    // Scenario outputs
    document.getElementById("calc-out-opt").textContent = formatINR(c.optimistic_profit);
    document.getElementById("calc-out-pess").textContent = formatINR(c.pessimistic_profit);
  } catch (err) {
    console.error("Calc error:", err);
  }
}

// 5. Human Approval Centre
async function loadApprovals() {
  try {
    const res = await fetch("/api/approvals");
    const list = await res.json();
    const container = document.getElementById("approvals-container");
    if (!container) return;
    container.innerHTML = "";

    if (list.length === 0) {
      container.innerHTML = `<div class="card" style="text-align:center; color: var(--text-muted); padding: 3rem;">No approval requests pending. System governance is clear.</div>`;
      return;
    }

    list.forEach(req => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div>
            <div style="display:flex; gap:0.5rem; align-items:center; margin-bottom:0.35rem;">
              <span class="badge badge-info">${req.action_type}</span>
              <span class="badge badge-${getStatusColor(req.status)}">${req.status}</span>
              <span style="font-size:0.75rem; color:var(--text-muted);">ID #${req.id} • ${req.created_at}</span>
            </div>
            <h3 style="font-size:1.15rem; font-weight:700;">${req.title}</h3>
            <div style="color:var(--text-secondary); font-size:0.85rem; margin-top:0.25rem;">Initiated by: <strong>${req.requested_by}</strong></div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Financial Outlay</div>
            <div style="font-size:1.4rem; font-weight:700; color:${req.financial_impact_inr > 0 ? 'var(--accent-warning)' : 'var(--text-primary)'};">${formatINR(req.financial_impact_inr)}</div>
          </div>
        </div>
        <div style="background:rgba(15,23,42,0.8); padding:0.85rem; border-radius:6px; margin:1rem 0; font-size:0.825rem;">
          <pre style="white-space:pre-wrap; margin:0; font-family:monospace;">${JSON.stringify(req.details, null, 2)}</pre>
        </div>
        ${req.decision_notes ? `<div style="font-size:0.8rem; color:var(--text-secondary); margin-bottom:0.75rem;"><strong>Decision Notes:</strong> ${req.decision_notes}</div>` : ''}
        <div style="display:flex; justify-content:flex-end; gap:0.5rem;">
          ${req.status === 'PENDING' ? `
            <button class="btn btn-sm btn-success" onclick="approveRequest(${req.id})">Approve Action</button>
            <button class="btn btn-sm btn-danger" onclick="promptRejectRequest(${req.id})">Reject</button>
          ` : ''}
          ${req.status === 'APPROVED' ? `
            <button class="btn btn-sm btn-primary" onclick="executeApprovedAction(${req.id})">Execute Action to Amazon SP-API</button>
          ` : ''}
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    showToast("Failed to load approvals: " + err.message, "danger");
  }
}

async function approveRequest(id) {
  try {
    const res = await fetch(`/api/approvals/${id}/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_name: "Abhishek (Admin)", notes: "Approved from human dashboard" })
    });
    if (res.ok) {
      showToast(`Request #${id} successfully approved!`, "success");
      loadApprovals();
      loadOverviewData();
    } else {
      const data = await res.json();
      showToast(data.detail || "Approval failed", "danger");
    }
  } catch (err) {
    showToast("Network error: " + err.message, "danger");
  }
}

function promptRejectRequest(id) {
  const reason = prompt("Enter mandatory rejection reason:");
  if (!reason) return;
  rejectRequest(id, reason);
}

async function rejectRequest(id, reason) {
  try {
    const res = await fetch(`/api/approvals/${id}/reject`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_name: "Abhishek (Admin)", reason })
    });
    if (res.ok) {
      showToast(`Request #${id} rejected.`, "info");
      loadApprovals();
      loadOverviewData();
    } else {
      const data = await res.json();
      showToast(data.detail || "Rejection failed", "danger");
    }
  } catch (err) {
    showToast("Network error: " + err.message, "danger");
  }
}

async function executeApprovedAction(id) {
  try {
    const res = await fetch(`/api/approvals/${id}/execute`, { method: "POST" });
    const data = await res.json();
    if (res.ok) {
      showToast(data.message || `Action #${id} executed!`, "success");
      loadApprovals();
      loadOverviewData();
    } else {
      showToast(data.detail || "Execution failed", "danger");
    }
  } catch (err) {
    showToast("Network error: " + err.message, "danger");
  }
}

// Emergency Stop Handler
async function toggleEmergencyStop() {
  if (state.emergencyStopActive) {
    if (!confirm("Are you sure you want to RESET the Emergency Stop and resume write operations?")) return;
    try {
      const res = await fetch("/api/approvals/emergency-stop/reset", { method: "POST" });
      const data = await res.json();
      state.emergencyStopActive = data.emergency_stop_active;
      updateEmergencyStopUI(false);
      showToast("Emergency Stop DISENGAGED. Write operations resumed.", "success");
    } catch (err) {
      showToast("Failed to reset emergency stop", "danger");
    }
  } else {
    const reason = prompt("Enter reason for Emergency Stop:", "Manual write freeze initiated by seller");
    if (!reason) return;
    try {
      const res = await fetch("/api/approvals/emergency-stop/trigger", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ triggered_by: "Abhishek (Admin)", reason })
      });
      const data = await res.json();
      state.emergencyStopActive = data.emergency_stop_active;
      updateEmergencyStopUI(true);
      showToast("EMERGENCY STOP ENGAGED! All write operations frozen.", "danger");
    } catch (err) {
      showToast("Failed to engage emergency stop", "danger");
    }
  }
}

function updateEmergencyStopUI(isActive) {
  const btn = document.getElementById("btn-emergency-stop");
  if (!btn) return;
  if (isActive) {
    btn.classList.add("active");
    btn.innerHTML = "⚠️ EMERGENCY STOP ENGAGED (RESET)";
  } else {
    btn.classList.remove("active");
    btn.innerHTML = "🛑 EMERGENCY STOP";
  }
}

// 6. Inventory Management Loader
async function loadInventory() {
  try {
    const res = await fetch("/api/inventory");
    const items = await res.json();
    const tbody = document.getElementById("inventory-table-tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    items.forEach(i => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${i.sku}</strong><br><span style="font-size:0.75rem; color:var(--text-muted);">${i.title.substring(0, 40)}...</span></td>
        <td>${i.current_stock} units</td>
        <td>${i.available_stock} units</td>
        <td>${i.daily_sales}/day</td>
        <td><strong style="color:${i.days_of_supply < 10 ? 'var(--accent-danger)' : 'var(--text-primary)'};">${i.days_of_supply} days</strong></td>
        <td>${i.reorder_point} units</td>
        <td>${i.safety_stock} units</td>
        <td>${i.needs_reorder ? `<span class="badge badge-danger">RESTOCK (${i.recommended_reorder_qty} units)</span>` : '<span class="badge badge-success">HEALTHY</span>'}</td>
        <td>
          <button class="btn btn-sm btn-primary" onclick="auditStock(${i.product_id})">Audit ROP</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    showToast("Inventory load failed: " + err.message, "danger");
  }
}

async function auditStock(productId) {
  showToast(`Auditing inventory and ROP for product #${productId}...`, "info");
  try {
    const res = await fetch(`/api/inventory/${productId}/audit`, { method: "POST" });
    const data = await res.json();
    if (res.ok) {
      showToast(`Inventory audit completed for ${data.sku}`, "success");
      loadInventory();
      loadOverviewData();
    }
  } catch (err) {
    showToast("Audit error: " + err.message, "danger");
  }
}

// 7. Listing Drafts
async function loadListings() {
  try {
    const res = await fetch("/api/listings");
    const drafts = await res.json();
    const container = document.getElementById("listings-container");
    if (!container) return;
    container.innerHTML = "";

    drafts.forEach(d => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem;">
          <div>
            <span class="badge badge-${getStatusColor(d.status)}">${d.status}</span>
            <h3 style="font-size:1.1rem; font-weight:700; margin-top:0.35rem;">${d.title}</h3>
            <div style="font-size:0.8rem; color:var(--text-secondary);">Brand: <strong>${d.brand}</strong> | Recommended Price: <strong>${formatINR(d.recommended_price_inr)}</strong></div>
          </div>
          <div>
            <button class="btn btn-sm btn-secondary" onclick="viewImagePlan(${d.product_id})">View 6-Slot Image Plan</button>
          </div>
        </div>
        <div style="margin-bottom:0.75rem;">
          <strong>Bullet Points:</strong>
          <ul style="padding-left:1.25rem; font-size:0.85rem; color:var(--text-secondary); margin-top:0.35rem;">
            ${d.bullets.filter(b => b).map(b => `<li style="margin-bottom:0.25rem;">${b}</li>`).join('')}
          </ul>
        </div>
        <div style="font-size:0.8rem; background:rgba(15,23,42,0.6); padding:0.6rem; border-radius:4px;">
          <strong>Backend Search Terms (${d.search_terms_bytes} / 249 bytes):</strong>
          <div style="color:var(--text-muted); margin-top:0.2rem;">${d.search_terms || 'None'}</div>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    showToast("Failed to load listings: " + err.message, "danger");
  }
}

async function viewImagePlan(productId) {
  try {
    const res = await fetch(`/api/listings/${productId}/images`);
    const data = await res.json();
    const modal = document.getElementById("image-plan-modal");
    const content = document.getElementById("image-plan-modal-content");
    if (!modal || !content) return;

    content.innerHTML = `
      <div style="margin-bottom:1rem; padding:0.75rem; background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.3); border-radius:6px; font-size:0.85rem;">
        <strong>Amazon India Image Guidelines:</strong> Slot 1 (MAIN) must be pure white background RGB(255,255,255), 1000px+ (1600px+ recommended for zoom), no text/watermarks.
      </div>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:1rem;">
        ${data.image_plan.map(slot => `
          <div style="background:rgba(15,23,42,0.8); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
              <span class="badge badge-info">Slot ${slot.slot}: ${slot.type}</span>
              <span style="font-size:0.7rem; color:var(--text-muted);">${slot.aspect_ratio} (${slot.target_resolution})</span>
            </div>
            <div style="font-weight:600; font-size:0.9rem; margin-top:0.25rem;">${slot.title}</div>
            <div style="font-size:0.75rem; color:var(--text-secondary); margin-top:0.35rem;">${slot.description}</div>
            <div style="margin-top:0.5rem; font-size:0.7rem; color:${slot.is_factual_photo ? 'var(--accent-success)' : 'var(--accent-purple)'};">
              ${slot.is_factual_photo ? '📷 Factual Photo Required' : '🎨 Promotional / Infographic Concept'}
            </div>
          </div>
        `).join('')}
      </div>
    `;
    modal.classList.add("active");
  } catch (err) {
    showToast("Error loading image plan: " + err.message, "danger");
  }
}

// 8. Daily Reports
async function loadDailyReports() {
  try {
    const res = await fetch("/api/reports");
    const reports = await res.json();
    const container = document.getElementById("reports-container");
    if (!container) return;
    container.innerHTML = "";

    reports.forEach(r => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
          <h3 style="font-size:1.1rem; font-weight:700;">Executive Briefing (${r.report_date})</h3>
          <span style="font-size:0.75rem; color:var(--text-muted);">${r.created_at}</span>
        </div>
        <pre style="white-space:pre-wrap; font-size:0.85rem; color:var(--text-primary); font-family:inherit; background:rgba(15,23,42,0.7); padding:1rem; border-radius:6px; margin:0;">${r.summary}</pre>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    showToast("Reports load failed: " + err.message, "danger");
  }
}

async function triggerGenerateReport() {
  showToast("Compiling daily report...", "info");
  try {
    const res = await fetch("/api/reports/generate", { method: "POST" });
    if (res.ok) {
      showToast("Daily report compiled successfully!", "success");
      loadDailyReports();
      loadOverviewData();
    }
  } catch (err) {
    showToast("Report generation error: " + err.message, "danger");
  }
}

// 9. Integrations Status & Vault
async function loadIntegrations() {
  try {
    const res = await fetch("/api/integrations/status");
    const status = await res.json();

    const spCard = document.getElementById("integration-spapi-status");
    if (spCard) {
      spCard.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
          <strong>Marketplace: ${status.amazon_sp_api.marketplace}</strong>
          <span class="badge ${status.amazon_sp_api.connected ? 'badge-success' : 'badge-warning'}">${status.amazon_sp_api.status}</span>
        </div>
        <p style="font-size:0.85rem; color:var(--text-secondary);">${status.amazon_sp_api.message || status.amazon_sp_api.error || ''}</p>
        <div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.35rem;">Marketplace ID: ${status.amazon_sp_api.marketplace_id}</div>
      `;
    }

    const aiCard = document.getElementById("integration-gemini-status");
    if (aiCard) {
      aiCard.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
          <strong>Engine: Gemini AI Studio (${status.gemini_api.model})</strong>
          <span class="badge ${status.gemini_api.connected ? 'badge-success' : 'badge-secondary'}">${status.gemini_api.status}</span>
        </div>
        <p style="font-size:0.85rem; color:var(--text-secondary);">${status.gemini_api.message}</p>
      `;
    }
  } catch (err) {
    console.error("Integrations load error:", err);
  }
}

// 10. Audit Logs Loader
async function loadAuditLogs() {
  try {
    const res = await fetch("/api/system/audit-logs");
    const logs = await res.json();
    const tbody = document.getElementById("audit-logs-tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    logs.forEach(l => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td style="font-size:0.75rem; color:var(--text-muted);">${l.timestamp}</td>
        <td><strong>${l.actor}</strong></td>
        <td><span class="badge badge-info">${l.action}</span></td>
        <td>${l.resource_type} #${l.resource_id || ''}</td>
        <td><pre style="margin:0; font-size:0.7rem; color:var(--text-secondary);">${JSON.stringify(l.details)}</pre></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    showToast("Audit logs error: " + err.message, "danger");
  }
}

// 11. Scheduler Cycle Trigger
async function triggerSchedulerCycle(cycleName) {
  showToast(`Starting ${cycleName} scheduler cycle...`, "info");
  try {
    const res = await fetch(`/api/system/scheduler/run-cycle?cycle=${cycleName}`, { method: "POST" });
    const data = await res.json();
    if (res.ok) {
      showToast(`${cycleName} cycle completed successfully!`, "success");
      loadOverviewData();
    } else {
      showToast(`Cycle failed: ${data.detail}`, "danger");
    }
  } catch (err) {
    showToast("Scheduler error: " + err.message, "danger");
  }
}

// Initialization on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  // Bind Nav Items
  document.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", () => {
      const section = item.getAttribute("data-section");
      if (section) navigateToSection(section);
    });
  });

  // Modal Closers
  document.querySelectorAll(".modal-close").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".modal-overlay").forEach(m => m.classList.remove("active"));
    });
  });

  // Initial Data Load
  loadOverviewData();
  recalculateLiveCalculator();
});
